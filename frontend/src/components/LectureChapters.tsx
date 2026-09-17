import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { BookOpen, ChevronLeft, ChevronRight, Layers, Lock } from "lucide-react";
import { MarkdownArticle } from "./MarkdownArticle";
import { ReadingProgressBar } from "./ReadingProgressBar";
import { Spoiler } from "./Spoiler";
import { CheatSheetBlock } from "./lecture/CheatSheetBlock";
import { AttachedTasks } from "./lecture/AttachedTasks";
import { LectureHeader } from "./lecture/LectureHeader";
import { StickyToc, type TocItem } from "./lecture/StickyToc";
import type { LectureData } from "../types";
import { readText, writeText } from "../utils/storage";

interface Chapter {
  index: number;
  heading: string;
  /** Первый абзац главы — «резюме одной строкой». */
  lead: string;
  body: string;
  /** Заголовки вида «Базовый код» / «Пример решения» — спрятать в спойлер. */
  spoiler: boolean;
}

interface LectureChaptersProps {
  markdown: string;
  taskId?: string;
  /** Метаданные лекции (description, cheatSheet, attachedTasks и т.п.) — опционально. */
  meta?: LectureData | null;
  /** Deep-link на задачу: открывает указанную тему и вкладку «Практические задания». */
  onOpenTask?: (taskId: string, lectureId: string) => void;
}

type Mode = "step" | "full";

const SPOILER_RE =
  /Базовый\s+код|Пример\s+(?:кода|решения)|полное\s+решение|код\s+решения|ответ|решение/i;

const CHAPTER_KEY = (taskId: string) => `lecture:chapter:${taskId}`;
const MODE_KEY = (taskId: string) => `lecture:mode:${taskId}`;

/** Разделяет markdown-лекцию на главы по «## Заголовкам». */
function parseChapters(markdown: string): Chapter[] {
  const chunks = markdown.split(/^##\s+/m);
  const chapters: Chapter[] = [];

  // Текст до первой «##» — обычно только заголовок документа «# …», — вырезаем.
  const preamble = chunks[0].replace(/^#\s+[^\r\n]*/m, "").trim();
  if (preamble) {
    chapters.push({
      index: 0,
      heading: "Введение",
      lead: extractLead(preamble.split(/\r?\n/)),
      body: preamble,
      spoiler: false,
    });
  }

  for (const raw of chunks.slice(1)) {
    const lines = raw.split(/\r?\n/);
    const heading = lines[0]?.trim();
    if (!heading) continue;
    const body = lines.slice(1).join("\n").trim();
    if (!body) continue;
    chapters.push({
      index: chapters.length,
      heading,
      lead: extractLead(lines.slice(1)),
      body,
      spoiler: SPOILER_RE.test(heading),
    });
  }
  return chapters;
}

/** Первый абзац (до пустой строки или структурного элемента) — для «Коротко:». */
function extractLead(lines: string[]): string {
  const parts: string[] = [];
  for (const line of lines) {
    const text = line.trim();
    if (!text) {
      if (parts.length > 0) break;
      continue;
    }
    if (/^(#|\||[>\-*`]|\d+\.)/.test(text)) break;
    parts.push(text);
    if (parts.join(" ").length >= 260) break;
  }
  return parts.join(" ");
}

function renderChapterBody(chapter: Chapter) {
  if (chapter.spoiler) {
    return (
      <Spoiler
        title={`${chapter.heading} — скрыто до попытки решения`}
        note="Сначала решите задания самостоятельно и отправьте решение — потом сверьтесь с этим кодом."
      >
        <MarkdownArticle markdown={chapter.body} />
      </Spoiler>
    );
  }
  return <MarkdownArticle markdown={chapter.body} />;
}

export function LectureChapters({ markdown, taskId, meta, onOpenTask }: LectureChaptersProps) {
  const chapters = useMemo(() => parseChapters(markdown), [markdown]);
  const storageId = taskId ?? "default";
  // Оглавление по главам (для ScrollSpy в режиме «весь текст»).
  const tocItems: TocItem[] = useMemo(
    () => chapters.map(ch => ({ id: `lecture-chapter-${ch.index}`, text: ch.heading, level: 2 })),
    [chapters],
  );

  const [mode, setMode] = useState<Mode>(() =>
    readText(MODE_KEY(storageId)) === "full" ? "full" : "step",
  );
  const [chapterIndex, setChapterIndex] = useState(() => {
    const saved = Number(readText(CHAPTER_KEY(storageId)) ?? "0");
    return Number.isFinite(saved) ? saved : 0;
  });
  const [fullIndex, setFullIndex] = useState(0);
  const sectionRefs = useRef<(HTMLElement | null)[]>([]);

  const safeIndex = Math.max(0, Math.min(chapterIndex, Math.max(chapters.length - 1, 0)));

  const changeChapter = useCallback(
    (next: number) => {
      if (chapters.length === 0) return;
      setChapterIndex(Math.max(0, Math.min(chapters.length - 1, next)));
    },
    [chapters.length],
  );

  // Сохраняем позицию чтения и режим в localStorage.
  useEffect(() => {
    writeText(CHAPTER_KEY(storageId), String(safeIndex));
  }, [storageId, safeIndex]);

  useEffect(() => {
    writeText(MODE_KEY(storageId), mode);
  }, [storageId, mode]);

  // Прогресс прокрутки в режиме «весь текст».
  useEffect(() => {
    if (mode !== "full") return;
    const observer = new IntersectionObserver(
      (entries) => {
        let best = -1;
        let bestRatio = 0;
        for (const entry of entries) {
          if (entry.isIntersecting && entry.intersectionRatio > bestRatio) {
            const idx = sectionRefs.current.indexOf(entry.target as HTMLElement);
            if (idx >= 0) {
              best = idx;
              bestRatio = entry.intersectionRatio;
            }
          }
        }
        if (best >= 0) setFullIndex(best);
      },
      { threshold: [0.05, 0.25, 0.5, 0.8] },
    );
    for (const el of sectionRefs.current) if (el) observer.observe(el);
    return () => observer.disconnect();
  }, [mode, chapters]);

  const jumpTo = useCallback(
    (index: number) => {
      if (mode === "step") {
        changeChapter(index);
        return;
      }
      document
        .getElementById(`lecture-chapter-${index}`)
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    },
    [mode, changeChapter],
  );

  if (chapters.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-8 text-slate-400 italic text-center">
        Материалы лекции готовятся.
      </div>
    );
  }

  const activeIndex =
    mode === "step" ? safeIndex : Math.max(0, Math.min(fullIndex, chapters.length - 1));
  const progressValue = (activeIndex + 1) / chapters.length;
  const progressLabel = `Глава ${activeIndex + 1} из ${chapters.length}`;
  const lastChapter = chapters[safeIndex] ?? null;

  return (
    <div className="animate-fadeIn">
      {/* Метаданные лекции: заголовок, длительность, сложность, теги, цели. */}
      {meta?.name &&
        (meta.description ||
          meta.durationMinutes ||
          meta.difficulty ||
          meta.tags?.length ||
          meta.learningOutcomes?.length) && (
        <LectureHeader
          title={meta.name}
          description={meta.description}
          durationMinutes={meta.durationMinutes}
          difficulty={meta.difficulty}
          tags={meta.tags}
          learningOutcomes={meta.learningOutcomes}
        />
      )}

      {/* Шапка: заголовок + переключатель режима */}
      <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 font-semibold text-slate-900">
          <BookOpen className="h-4 w-4 text-indigo-600" />
          Чтение лекции
        </div>
        <div className="flex items-center gap-1 self-start rounded-xl border border-slate-200 bg-white p-1 shadow-sm">
          <button
            type="button"
            onClick={() => setMode("step")}
            className={`rounded-lg px-3 py-1.5 text-xs font-medium transition cursor-pointer ${
              mode === "step" ? "bg-indigo-600 text-white shadow" : "text-slate-500 hover:bg-slate-100"
            }`}
          >
            По шагам
          </button>
          <button
            type="button"
            onClick={() => setMode("full")}
            className={`rounded-lg px-3 py-1.5 text-xs font-medium transition cursor-pointer ${
              mode === "full" ? "bg-indigo-600 text-white shadow" : "text-slate-500 hover:bg-slate-100"
            }`}
          >
            Весь текст
          </button>
        </div>
      </div>

      {/* Прогресс чтения */}
      <ReadingProgressBar value={progressValue} />
      <p className="mt-1.5 text-[11px] text-slate-500">{progressLabel}</p>

      {/* Мобильное оглавление (горизонтальные чипы) */}
      <div className="no-scrollbar -mx-1 mt-4 flex gap-1.5 overflow-x-auto px-1 pb-2 lg:hidden">
        {chapters.map((chapter) => (
          <button
            key={chapter.index}
            type="button"
            onClick={() => jumpTo(chapter.index)}
            className={`flex shrink-0 items-center gap-1 rounded-full border px-3 py-1 text-xs transition cursor-pointer ${
              chapter.index === activeIndex
                ? "border-indigo-300 bg-indigo-100 text-indigo-700 font-medium"
                : "border-slate-200 bg-white text-slate-500 hover:bg-slate-50"
            }`}
          >
            {chapter.spoiler && <Lock className="h-3 w-3" />}
            {chapter.index + 1}. {chapter.heading}
          </button>
        ))}
      </div>

      <div className="mt-5 grid gap-6 lg:grid-cols-[minmax(0,220px)_minmax(0,1fr)]">
        {/* Боковое оглавление (lg+) */}
        <aside className="hidden lg:block">
          <div className="lg:sticky lg:top-2">
            <div className="mb-2 flex items-center gap-1.5 text-[11px] uppercase tracking-wider text-slate-500">
              <Layers className="h-3.5 w-3.5" /> Оглавление
            </div>
            {mode === "full" ? (
              <StickyToc items={tocItems} />
            ) : (
              <nav className="space-y-1">
                {chapters.map((chapter) => (
                  <button
                    key={chapter.index}
                    type="button"
                    onClick={() => jumpTo(chapter.index)}
                    className={`flex w-full items-center gap-2 rounded-lg px-3 py-1.5 text-left text-[13px] leading-snug transition cursor-pointer border ${
                      chapter.index === activeIndex
                        ? "bg-indigo-50 border-indigo-200 font-medium text-indigo-700 shadow-sm"
                        : "border-transparent text-slate-500 hover:bg-slate-100 hover:text-slate-800"
                    }`}
                  >
                    {chapter.spoiler && <Lock className="h-3 w-3 shrink-0 text-slate-400" />}
                    {chapter.index === activeIndex && (
                      <span className="absolute left-0 h-4 w-0.5 rounded-r bg-indigo-600" />
                    )}
                    <span className="min-w-0 truncate">{chapter.heading}</span>
                  </button>
                ))}
              </nav>
            )}
          </div>
        </aside>

        <div className="min-w-0">
          {mode === "step" ? (
            <div className="space-y-4">
              <article className="rounded-2xl border border-slate-200 bg-white p-6">
                <h2 className="mb-4 flex items-center gap-2 text-xl font-bold text-slate-900">
                  {lastChapter?.heading}
                  {lastChapter?.spoiler && <Lock className="h-4 w-4 shrink-0 text-slate-400" />}
                </h2>

                {lastChapter && !lastChapter.spoiler && lastChapter.lead && (
                  <div className="mb-4 rounded-lg border border-indigo-200 bg-indigo-50 px-4 py-2.5 text-sm leading-relaxed text-indigo-900">
                    <span className="font-semibold text-indigo-800">Коротко: </span>
                    {lastChapter.lead}
                  </div>
                )}

                {lastChapter && renderChapterBody(lastChapter)}
              </article>

              <div className="flex items-center justify-between gap-3">
                <button
                  type="button"
                  onClick={() => changeChapter(safeIndex - 1)}
                  disabled={safeIndex === 0}
                  className="flex items-center gap-1.5 rounded-xl border border-slate-300 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40 cursor-pointer"
                >
                  <ChevronLeft className="h-4 w-4" />
                  Назад
                </button>

                {safeIndex < chapters.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => changeChapter(safeIndex + 1)}
                    className="flex items-center gap-1.5 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 cursor-pointer"
                  >
                    Дальше
                    <ChevronRight className="h-4 w-4" />
                  </button>
                ) : (
                  <span className="text-xs text-slate-500">
                    Это последняя глава — переходите к практическим заданиям.
                  </span>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-8">
              {chapters.map((chapter, idx) => (
                <article
                  key={chapter.index}
                  id={`lecture-chapter-${chapter.index}`}
                  ref={(el) => {
                    sectionRefs.current[chapter.index] = el;
                  }}
                  className="scroll-mt-40 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
                >
                  <h2 className="mb-4 flex items-center gap-2 text-xl font-bold text-slate-900">
                    {chapter.heading}
                    {chapter.spoiler && <Lock className="h-4 w-4 shrink-0 text-slate-400" />}
                  </h2>
                  {renderChapterBody(chapter)}
                  {idx < chapters.length - 1 && (
                    <div className="mt-6 pt-4 text-center text-slate-300">···</div>
                  )}
                </article>
              ))}
            </div>
          )}

          {/* Шпаргалка и привязанные задачи — в конце лекции. */}
          {meta?.cheatSheet && <CheatSheetBlock data={meta.cheatSheet} />}
          {(meta?.attachedTasks ?? []).length > 0 && onOpenTask && (
            <AttachedTasks
              tasks={meta?.attachedTasks ?? []}
              problems={meta?.problems ?? []}
              onOpenTask={onOpenTask}
            />
          )}
        </div>
      </div>
    </div>
  );
}