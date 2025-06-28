# 📡 HTTP Server — OTUS Homework

## 📄 Описание
Самописный HTTP-сервер на Python, реализующий базовую поддержку протокола HTTP/1.1:

- Обработка методов `GET` и `HEAD`
- Отдача статичных файлов
- Обработка ошибок 404 и 405
- Поддержка контента: `.html`, `.css`, `.js`, `.jpg`, `.png`, и др.

## ⚙️ Запуск

```bash
python httpd.py --doc-root ./static
```

## 🏗️ Архитектура

- Классовая модель TCP-сервера (`TCPServer`)
- Обработка одного клиента за итерацию: `accept → recv → send → close`

## 📊 Нагрузочное тестирование

**Инструмент**: Apache Benchmark (`ab`)

**Команда**:
```bash
ab -n 50000 -c 100 -r http://localhost:8080/
```

**Результат:**
```
Requests per second:    12.13 [#/sec] (mean)
Time per request:       8244 ms (mean)
Failed requests:        0
```

## 🗂️ Структура проекта

```
homework_6_html_server/
├── homework/
├── pages_folder/
├── src/
│   ├── __init__.py
│   ├── httpd.py
│   ├── logger.py
│   ├── main.py
│   └── utils.py
├── README.md
└── pyproject.toml

```