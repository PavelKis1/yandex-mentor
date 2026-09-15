
const CACHE_PREFIX = "yandex_mentor_";

export function getCache<T>(key: string): T | null {
  const data = localStorage.getItem(CACHE_PREFIX + key);
  if (!data) return null;
  try {
    return JSON.parse(data) as T;
  } catch {
    return null;
  }
}

export function setCache<T>(key: string, data: T): void {
  localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(data));
}

export function removeCache(key: string): void {
  localStorage.removeItem(CACHE_PREFIX + key);
}

export function clearAllCache(): void {
  Object.keys(localStorage)
    .filter((key) => key.startsWith(CACHE_PREFIX))
    .forEach((key) => localStorage.removeItem(key));
}
