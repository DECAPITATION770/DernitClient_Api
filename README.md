# Deribit API Client

---

## Deployment

### Requirements
- Docker
- Docker Compose


### Clone Repository
```bash
git clone https://github.com/DECAPITATION770/DernitClient_Api.git
cd DernitClient_Api
```
### Run
```bash
cp .env.example .env
docker-compose up -d
````

### Access

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---
## Design Decisions



### ⚙️ FastAPI
HTTP API слой приложения.  
Используется для маршрутизации запросов, валидации данных и генерации OpenAPI спецификации.



### ⏱ Celery
Фоновый обработчик периодических задач.  
Отвечает за регулярное получение цен и работает независимо от HTTP API.



### 🗄 PostgreSQL
Основное хранилище данных.  
Используется для хранения исторических цен и временных рядов.



### 🧩 Service + Repository
Архитектурное разделение слоёв.  
Бизнес-логика изолирована от доступа к данным и ORM.



### 🌐 aiohttp
Асинхронный HTTP-клиент.  
Используется для неблокирующих запросов к Deribit API.



### 🕒 UNIX timestamp
Формат хранения времени.  
Исключает проблемы с таймзонами и упрощает фильтрацию по диапазонам.
