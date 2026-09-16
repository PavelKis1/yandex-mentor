"""Данные блока 21: Префиксное дерево (Trie)."""
from genlib import run

LECTURE_SLUG = "21_trie"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "21",
        "slug": "trie",
        "title": "Префиксное дерево (Trie)",
        "description": "Trie — дерево, где путь от корня к узлу кодирует префикс строки. Разбираем поиск слов на сетке (Word Search II), замену слов на корни и максимальный XOR пары через побитовый прием.",
        "durationMinutes": 15,
        "difficulty": "middle",
        "tags": ["Algorithms", "Trie", "Strings", "Bit Manipulation"],
        "learningOutcomes": [
            "Строить Trie из набора строк с узлами-словарями",
            "Применять Trie для сокращения DFS по сетке слов",
            "Использовать префиксное дерево для замены слов корнями",
            "Находить максимальный XOR пары жадной/битовой техникой"
        ],
        "complexity": {
            "timeComplexity": "O(N * L)",
            "spaceComplexity": "O(N * L)",
            "explanation": "Операции зависят от суммарной длины слов, а не от числа совпадений; Trie хранит по одному узлу на символ."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "В чём преимущество Trie при поиске слов на сетке?",
                "options": [
                    {"id": "opt1", "text": "Обрезает ветви DFS, если префикса нет в словаре", "isCorrect": True, "explanation": "DFS длиной в полное слово не выполняется для несуществующих префиксов."},
                    {"id": "opt2", "text": "Хранит слова в памяти быстрее, чем список", "isCorrect": False, "explanation": "Главная выгода — быстрый поиск по префиксу, не экономия памяти."},
                    {"id": "opt3", "text": "Сортирует слова автоматически", "isCorrect": False, "explanation": "Сортировка не является свойством Trie."}
                ],
                "hint": "Как Trie помогает ускорить перебор префиксов?"
            },
            {
                "id": "q2",
                "question": "Какой приём для максимального XOR пары используют битовый жадный перебор?",
                "options": [
                    {"id": "opt1", "text": "Собирать префиксы старших битов и проверять кандидата", "isCorrect": True, "explanation": "Старшие биты важнее, поэтому считаем лучший результат по битам сверху вниз."},
                    {"id": "opt2", "text": "Сложить все числа без знака", "isCorrect": False, "explanation": "Сумма не даёт XOR."},
                    {"id": "opt3", "text": "Искать пару с минимальной разницей", "isCorrect": False, "explanation": "Минимум разницы не равен максимуму XOR."}
                ],
                "hint": "Какой бит важнее: старший или младший?"
            }
        ],
        "attachedTasks": [
            {"taskId": "21-p1", "title": "Слова на доске", "difficulty": "easy", "slug": "word-search-ii"},
            {"taskId": "21-p2", "title": "Замена слов", "difficulty": "medium", "slug": "replace-words"},
            {"taskId": "21-p3", "title": "Максимальный XOR", "difficulty": "hard", "slug": "maximum-xor-of-two-numbers"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Trie: узлы с детьми и флагом конца слова; O(L) на вставку/поиск.",
                "Поиск на сетке: DFS от каждой клетки, отсечение по отсутствию префикса в Trie.",
                "Замена слов: кратчайший префикс, встречающийся в словаре.",
                "Максимальный XOR: перебор старших битов, проверка кандидата по префиксам.",
                "Используйте множество для быстрого ответа о совпадении префикса."
            ]
        }
    },
"problems": [
{
            "id": "21-p1", "title": "Слова на доске", "difficulty": "easy",
            "lecture_id": "21", "order": 1, "entry_function": "find_words",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def find_words(board: list[list[str]], words: list[str]) -> list[str]:\n    \"\"\"Все слова из words, которые можно составить по соседним клеткам доски.\"\"\"\n    ...",
            "description": "Дана доска `board` из букв `m x n` и список `words`. Слово можно составить, если его буквы **соседние по горизонтали/вертикали** (каждую клетку используют не более одного раза). Верните **список найденных слов в алфавитном порядке**.\n\n**Функция решения:**\n\n```python\ndef find_words(board: list[list[str]], words: list[str]) -> list[str]:\n    ...\n```",
            "examples": [
                {"input": "board=[['o','a','a','n'],['e','t','a','e'],['i','h','k','r'],['i','f','l','v']], words=['oath','pea','eat','rain']", "output": "['eat', 'oath']", "explanation": "Только 'eat' и 'oath' можно составить по доске."},
                {"input": "board=[['a']], words=['a']", "output": "['a']", "explanation": "Одна клетка — одно слово."},
                {"input": "board=[], words=['a']", "output": "[]", "explanation": "Пустая доска — ничего не найдено."}
            ],
            "constraints": ["0 ≤ m, n ≤ 10", "0 ≤ len(words) ≤ 1000", "Буквы — строчные латинские"],
            "hints": [
                "Постройте Trie всех искомых слов.",
                "DFS от каждой клетки повторно не посещает (временно помечайте клетку).",
                "Верните результат отсортированным.",
                "Используйте set, чтобы не было дубликатов."
            ],
            "args": [
                [[], ["a"]],
                [[["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]], ["oath", "pea", "eat", "rain"]],
                [[["a"]], ["b"]],
                [[["a"]], ["a"]],
                [[["a", "a"]], ["a"]],
                [[["a", "b"]], ["ab", "ba"]],
                [[[]], ["abc"]],
                [[["a", "b"], ["c", "d"]], ["ab", "cd", "abc", "dc", "a", "d"]]
            ],
            "hidden": [True, False, True, False, True, True, True, True]
        },
        {
            "id": "21-p2", "title": "Замена слов", "difficulty": "medium",
            "lecture_id": "21", "order": 2, "entry_function": "replace_words",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def replace_words(dictionary: list[str], sentence: str) -> str:\n    \"\"\"Заменить каждое слово предложения на кратчайший корень из dictionary.\"\"\"\n    ...",
            "description": "Дан словарь корней `dictionary` и предложение `sentence`. Для каждого слова предложения, если оно **начинается с корня** из словаря, замените его **кратчайшим** таким корнем; иначе оставьте слово как есть. Верните преобразованное предложение.\n\n**Функция решения:**\n\n```python\ndef replace_words(dictionary: list[str], sentence: str) -> str:\n    ...\n```",
            "examples": [
                {"input": "dictionary=['cat','bat','rat'], sentence='the cattle was rattled by the battery'", "output": "'the cat was rat by the bat'", "explanation": "'cattle'→'cat', 'rattled'→'rat', 'battery'→'bat'."},
                {"input": "dictionary=[], sentence='hello world'", "output": "'hello world'", "explanation": "Корней нет — ничего не меняется."},
                {"input": "dictionary=['a'], sentence='apple ant'", "output": "'a a'", "explanation": "Кратчайший корень 'a' заменяет 'apple' и 'ant'."}
            ],
            "constraints": ["0 ≤ len(dictionary) ≤ 1000", "Предложение из слов через пробел"],
            "hints": [
                "Сложите корни в set для проверки за O(1).",
                "Для каждого слова накапливайте префикс, пока он не станет корнем.",
                "Учитывайте кратчайший корень: останавливайтесь на первом найденном."
            ],
            "args": [
                [["cat", "bat", "rat"], "the cattle was rattled by the battery"],
                [[], "hello world"],
                [["a"], "apple ant"],
                [["cat", "cat"], "the cattle"],
                [["c", "catch"], "cattle"],
                [["a"], ""],
                [["cat"], "cat"]
            ],
            "hidden": [False, True, False, True, True, True, True]
        },
{
            "id": "21-p3", "title": "Максимальный XOR", "difficulty": "hard",
            "lecture_id": "21", "order": 3, "entry_function": "find_max_xor",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def find_max_xor(nums: list[int]) -> int:\n    \"\"\"Максимальный XOR двух чисел из nums.\"\"\"\n    ...",
            "description": "Дан массив целых чисел `nums`. Верните **максимальный XOR** двух чисел из массива.\n\n**Функция решения:**\n\n```python\ndef find_max_xor(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [3, 10, 5, 25, 2, 8]", "output": "28", "explanation": "25 XOR 5 = 28 — максимальная пара."},
                {"input": "nums = [0]", "output": "0", "explanation": "Единственное число XOR с самим собой = 0."},
                {"input": "nums = [8, 10, 2]", "output": "10", "explanation": "8 XOR 2 = 10."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 10^5", "0 ≤ nums[i] < 2^31"],
            "hints": [
                "Перебирайте старшие биты и проверяйте, можно ли получить кандидата.",
                "Держите множество префиксов чисел по текущей маске.",
                "Если пара p, p^cand в префиксах — бит достижим."
            ],
            "args": [
                [3, 10, 5, 25, 2, 8],
                [0],
                [1],
                [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70],
                [4, 6, 7],
                [5, 25],
                [8, 10, 2]
            ],
            "wrap_single": True,
            "hidden": [False, True, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])