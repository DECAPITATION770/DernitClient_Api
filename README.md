# Deribit API Client
![Python](https://img.shields.io/badge/python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Celery](https://img.shields.io/badge/Celery-37823B?style=flat&logo=celery&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/github/license/DECAPITATION770/DernitClient_Api?style=flat)

Асинхронный сервис, который **раз в минуту** забирает *index price* BTC/USD и ETH/USD с биржи Deribit и сохраняет данные в PostgreSQL.

Проект разделён на:

* HTTP API для чтения данных
* фоновый сборщик цен

Всё запускается одной командой через Docker.

---

## TL;DR

* Celery раз в минуту получает цены с Deribit
* FastAPI отдаёт сохранённые данные
* PostgreSQL хранит time-series
* Сбор данных и API полностью изолированы
* Docker-first, без ручной возни

---

## Quick Start

```bash
git clone https://github.com/DECAPITATION770/DernitClient_Api.git
cd DernitClient_Api
cp .env.example .env
docker-compose up -d --build
```

Открыть Swagger:
[http://localhost:8000/docs](http://localhost:8000/docs)

<details>
<summary><strong>Запуск без Docker (Manual Run)</strong></summary>

Для локального запуска без использования Docker.

### Backend API

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Доступ к API:
[http://localhost:8000/docs](http://localhost:8000/docs)

### Celery Worker

```bash
celery -A app.celery_app worker -l info
```

### Celery Beat

```bash
celery -A app.celery_app beat -l info
```

</details>

---

## What’s Running

* FastAPI → [http://localhost:8000](http://localhost:8000)
* PostgreSQL → internal
* Redis → internal
* Celery worker → background
* Celery beat → background

Если Swagger открывается — система жива.

---

## Tech Stack

* **Python 3.11** — async runtime
* **FastAPI** — HTTP API
* **Celery + Redis** — фоновый сбор цен
* **PostgreSQL** — хранение данных
* **aiohttp** — Deribit API client
* **Docker / Docker Compose** — изоляция и запуск
* **pytest** — тестирование

---

## Architecture

### Logical Flow

```text
Deribit API
     ↓
DeribitClient (aiohttp)
     ↓
PriceService
     ↓
PriceRepository
     ↓
PostgreSQL
```

### Runtime Overview

```text
┌─────────────┐     ┌──────────────┐
│ FastAPI     │     │ Celery Beat  │
│ (HTTP API)  │     └──────┬───────┘
└──────┬──────┘            ↓
       ↓             ┌──────────────┐
┌─────────────┐      │ Celery Worker│
│ PostgreSQL  │      └──────┬───────┘
└─────────────┘             ↓
                       Deribit API
```

---

## Example Flow (Happy Path)

1. Celery Beat запускает задачу раз в минуту
2. DeribitClient получает index price
3. Цена сохраняется в PostgreSQL
4. API отдаёт данные через HTTP

---

## API Overview

| Endpoint                     | Description    |
| ---------------------------- | -------------- |
| GET `/api/v1/prices`         | История цен    |
| GET `/api/v1/prices/latest`  | Последняя цена |
| GET `/api/v1/prices/by-date` | Цены за период |

---

### Получить последнюю цену

```http
GET /api/v1/prices/latest?ticker=BTC_USD
```

```json
{
  "id": 29,
  "ticker": "BTC_USD",
  "price": 95131.86,
  "timestamp": 1768752407
}
```

**Errors**

* `404` — данных по тикеру нет

---

### История цен

```http
GET /api/v1/prices?ticker=ETH_USD&limit=100
```

```json
[
  {
    "id": 28,
    "ticker": "ETH_USD",
    "price": 3334.38,
    "timestamp": 1768752345
  }
]
```

---

### Цены за период

```http
GET /api/v1/prices/by-date?ticker=BTC_USD&date_from=1768751800&date_to=1768752400
```

```json
[
  {
    "id": 12,
    "ticker": "BTC_USD",
    "price": 95012.12,
    "timestamp": 1768751844
  }
]
```

**Errors**

* `400` — `date_from > date_to`

---

## Error Handling

| Code | Reason                    |
| ---- | ------------------------- |
| 400  | Некорректные параметры    |
| 404  | Данные не найдены         |
| 500  | Внутренняя ошибка сервиса |

---

## Design Decisions

### FastAPI

* Асинхронная обработка запросов
* Валидация входных данных
* OpenAPI документация из коробки

### Celery

* Гарантированное выполнение задач
* Retry при сбоях Deribit API
* Фоновые задачи не блокируют HTTP API

### Service / Repository

* Бизнес-логика не зависит от БД
* Упрощённое тестирование
* Минимальная связность слоёв

### UNIX Timestamp

* Нет проблем с таймзонами
* Удобная фильтрация
* Стандарт для time-series данных

---

## Testing

### Через Docker (рекомендуется)

```bash
docker-compose exec app pytest -v
```

### Локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

---

## Failure Handling

* Deribit API недоступен → Celery retry
* Ошибки сети → повторная попытка
* Некорректные параметры API → 400
* Отсутствие данных → 404

---

## Assumptions & Limitations

* Хранится только index price
* Поддерживаются только BTC/USD и ETH/USD
* Частота сбора фиксированная (1 минута)
