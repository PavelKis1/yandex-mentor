// API конфигурация.
// VITE_API_URL задаётся через frontend/.env (VITE_API_URL=https://...) или env-переменной при сборке.
// По умолчанию — локальный сервер ментора.
const DEFAULT_API_BASE = "http://localhost:8000";

export const API_BASE: string = import.meta.env?.VITE_API_URL || DEFAULT_API_BASE;