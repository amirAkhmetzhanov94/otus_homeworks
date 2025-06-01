# 🧠 Scoring API

Мини-сервис для обработки HTTP POST-запросов на скоринг пользователей и получения интересов по id.  
Задание из курса OTUS.

---

## 🚀 Запуск

```bash
python api.py -p 8080
```

Для логирования в файл:

```bash
python api.py -p 8080 -l my_log_file.txt
```

---

## 🧪 Запуск тестов

Убедитесь, что вы находитесь в корне проекта и у вас есть файл `test.py`.  
Для запуска всех тестов:

```bash
python test_1.py
```

Для подробного вывода:

```bash
python -m unittest test_1.py -v
```

---

## 🔑 Аутентификация

* Для обычных пользователей токен = `sha512(account + login + SALT)`
* Для админа токен = `sha512(datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT)`
* `SALT = "Otus"`, `ADMIN_SALT = "42"`

---

## 🧪 Примеры запросов

### `online_score`

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "account": "horns&hoofs",
  "login": "h&f",
  "method": "online_score",
  "token": "<valid_token>",
  "arguments": {
    "phone": "79175002040",
    "email": "stupnikov@otus.ru"
  }
}' http://127.0.0.1:8080/method/
```

Ответ:

```json
{"code": 200, "response": {"score": 5.0}}
```

Для админа:

```json
{"code": 200, "response": {"score": 42}}
```

---

### `clients_interests`

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "account": "horns&hoofs",
  "login": "admin",
  "method": "clients_interests",
  "token": "<admin_token>",
  "arguments": {
    "client_ids": [1, 2, 3],
    "date": "01.01.2023"
  }
}' http://127.0.0.1:8080/method/
```

Ответ:

```json
{"code": 200, "response": {"1": ["books", "hi-tech"], "2": ["pets", "tv"], "3": ["travel", "music"]}}
```

---

## 📦 Структура проекта

* `api.py` — главный сервер и обработка запросов
* `scoring.py` — логика скоринга и интересов
* `exceptions.py` — исключения
* `test.py` — тесты

---

## 🧠 Особенности

* Метакласс собирает поля модели запроса
* Поддержка nullable и required полей
* Общая структура запроса — декларативная и проверяемая
* Ответы строго по формату `{"code": ..., "response": ...}` или `{"error": ..., "code": ...}`
