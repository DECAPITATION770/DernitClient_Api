<div align="center">

# Deribit Price Tracker

**Асинхронный трекер index price BTC/USD и ETH/USD**  
сбор каждые 60 секунд → PostgreSQL → удобный FastAPI API

[![Python 3.11](https://img.shields.io/badge/python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Celery](https://img.shields.io/badge/Celery-37823B?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

<p align="center">
  <img src="docs/images/deribit_logo_dark.svg" alt="Deribit Price Tracker Banner" width="800"/>
  <br/><br/>
  <em>Реал-тайм цены крипты без лишних зависимостей — одна команда и готово</em>
</p>

## Почему стоит попробовать

- ⚡ Полностью асинхронный стек (FastAPI + aiohttp + Celery)
- 🕒 Автособор index price **каждые 60 секунд**
- 📊 Надёжное хранение time-series в PostgreSQL
- 🔍 Красивая интерактивная документация (Swagger + ReDoc)
- 🐳 Всё запускается одной командой через Docker Compose
- 🔄 Автоматические ретраи при сбоях биржи
- 🧪 Тесты + чёткая слоистая архитектура

## Быстрый старт (рекомендуется)

```bash
# 1. Клонируем репозиторий
git clone https://github.com/DECAPITATION770/DernitClient_Api.git
cd DernitClient_Api

# 2. Копируем переменные окружения
cp .env.example .env

# 3. Запускаем (первый раз ~1–2 минуты наビルд)
docker compose up -d --build

# 4. Ждём 30–60 секунд пока соберутся первые данные
# Затем открываем в браузере:
# → http://localhost:8000/docs          (Swagger UI)
# → http://localhost:8000/redoc         (альтернативная документация)
```

Проверить, что всё живо:

```bash
curl http://localhost:8000/api/v1/prices/latest?ticker=BTC_USD | jq
```

Ожидаемый ответ:

```json
{
  "id": 42,
  "ticker": "BTC_USD",
  "price": 95131.86,
  "timestamp": 1768752407
}
```

## Как это выглядит

<p align="center">
  <img src="docs/images/swagger-dark.png" alt="Swagger UI — цены в реальном времени" width="800"/>
  <br/><br/>
  <em>Интерактивная документация FastAPI с примерами запросов</em>
</p>

<p align="center">
  <img src="docs/images/price-chart-example.png" alt="График цен BTC/USD и ETH/USD" width="800"/>
  <br/><br/>
  <em>Пример time-series данных (можно легко подключить Grafana)</em>
</p>

<p align="center">
  <img src="docs/images/architecture-diagram.png" alt="Архитектура сервиса" width="800"/>
  <br/><br/>
  <em>Как всё связано: Deribit → Celery → PostgreSQL → FastAPI</em>
</p>

## API — основные эндпоинты

| Метод | Эндпоинт                              | Описание                     | Пример запроса                              |
|-------|---------------------------------------|------------------------------|---------------------------------------------|
| GET   | `/api/v1/prices/latest`               | Последняя цена               | `?ticker=BTC_USD`                           |
| GET   | `/api/v1/prices`                      | История (последние N записей)| `?ticker=ETH_USD&limit=100`                 |
| GET   | `/api/v1/prices/by-date`              | Цены за временной диапазон   | `?ticker=BTC_USD&date_from=1768750000&date_to=1768753000` |

### Примеры с curl

**Последняя цена**

```bash
curl "http://localhost:8000/api/v1/prices/latest?ticker=BTC_USD" \| jq
```

**Последние 50 значений ETH**

```bash
curl "http://localhost:8000/api/v1/prices?ticker=ETH_USD&limit=50" \| jq
```

**Диапазон дат**

```bash
curl "http://localhost:8000/api/v1/prices/by-date?ticker=BTC_USD&date_from=1768740000&date_to=1768760000" \| jq
```

## Технический стек

- **Python** 3.11 (async/await везде)
- **FastAPI** + **Pydantic** — API и валидация
- **Celery** + **Redis** — планировщик и брокер
- **PostgreSQL** — основное хранилище time-series
- **aiohttp** — клиент к Deribit API
- **SQLAlchemy 2.0** + **asyncpg** — асинхронный ORM
- **Docker Compose** — всё в контейнерах
- **pytest** + **pytest-asyncio** — тесты

## Архитектура (логический поток)

```text
Deribit WebSocket/REST API
          ↓ (aiohttp)
     DeribitClient
          ↓
    PriceService
          ↓
 PriceRepository (SQLAlchemy async)
          ↓
     PostgreSQL
          ↑
      FastAPI → HTTP ответы
```

Фоновая часть полностью изолирована от HTTP-слоя — даже если Deribit ляжет, API продолжает отдавать кэшированные данные.

## Тестирование

Через Docker (самый удобный способ):

```bash
docker compose exec app pytest -v
```

Локально:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```
