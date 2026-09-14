/** Нормализует неизвестную ошибку (throw-значение) в строку для отображения. */
export function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : String(err);
}