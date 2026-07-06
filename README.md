# Как запустить

## 1. Запуск через Docker

```bash
docker compose up --build
```

После запуска сервис будет доступен:

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Elasticsearch: [http://localhost:9200](http://localhost:9200)
* PostgreSQL: localhost:5432


## 2. Загрузка данных (CSV)

```http
POST /admin/load
```
Через эту ручку подгружаем файл.

### Описание:

Загрузка CSV файла в систему (PostgreSQL и Elasticsearch)

### Form-data:

* file: CSV файл

### Пример:

```bash
curl -X POST "http://localhost:8000/admin/load" \
  -F "file=@documents.csv"
```


# API ручки

## Поиск документов

```http
GET /documents/search?q={text}
```

### Описание:

Поиск документов по тексту через Elasticsearch

### Ответ:

```json
[
  {
    "id": 1,
    "rubrics": ["VK-..."],
    "text": "пример текста",
    "created_date": "2019-07-25T12:42:13"
  }
]
```

---

## Удаление документа

```http
DELETE /documents/{id}
```

### Описание:

Удаляет документ из PostgreSQL и Elasticsearch

### Ответ:

```json
{
  "status": "deleted"
}
```

---

# 📁 Структура проекта

```text
app/
├── main.py                 # точка входа FastAPI
├── models.py               # SQLAlchemy модели
├── schemas.py              # Pydantic схемы
├── database.py             # подключение к PostgreSQL
├── config.py               # настройки (env)
├── dependencies.py         # зависимости FastAPI

├── services/
│   └── elastic.py         # работа с Elasticsearch

├── routers/
│   ├── documents.py       # поиск и удаление
│   └── admin.py           # загрузка CSV

└── loader.py              # CLI загрузка CSV
```

## Есть документация docs.json

## Запуск тестов через Docker

```bash
docker compose exec api pytest -q
```
