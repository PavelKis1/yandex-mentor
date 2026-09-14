# Лекция: 44 — Протокол HTTP (HyperText Transfer Protocol)

## Обзор темы
HTTP — прикладной протокол передачи данных, лежащий в основе взаимодействия клиентских приложений (браузеры, мобильные клиенты) и серверных микросервисов.

---

## Подробный теоретический минимум

### 1. Методы HTTP и идемпотентность
- **`GET`**: запросы на чтение данных (идемпотентный, безопасный).
- **`POST`**: создание нового ресурса (не идемпотентный).
- **`PUT`**: полная замена или создание ресурса (идемпотентный).
- **`PATCH`**: частичное обновление ресурса (часто идемпотентный).
- **`DELETE`**: удаление ресурса (идемпотентный).
*Идемпотентность* означает, что многократное выполнение одного и того же запроса приводит к тому же результату на сервере.

### 2. Коды состояния (Status Codes)
- **`2xx` (Success)**: 200 OK, 201 Created, 204 No Content.
- **`3xx` (Redirection)**: 301 Moved Permanently, 304 Not Modified.
- **`4xx` (Client Error)**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests.
- **`5xx` (Server Error)**: 500 Internal Server Error, 502 Bad Gateway, 504 Gateway Timeout.

---

## Производственный пример кода

Пример простого HTTP-сервера на стандартной библиотеке Python (`http.server`):

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "ok"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), SimpleHTTPHandler)
    print("HTTP Server running on port 8080...")
    # server.serve_forever() # Запуск сервера
```

---

## Анализ сложности (Big O)

- Транспорт данных по сети зависит от размера полезной нагрузки ($O(N)$ по размеру тела запроса/ответа).

---

## Применение в Яндексе
- **Межсервисное взаимодействие**: Все микросервисы в Яндексе общаются по протоколам HTTP/1.1, HTTP/2 и gRPC.

