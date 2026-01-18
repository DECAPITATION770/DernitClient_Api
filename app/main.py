from fastapi import FastAPI
from app.api.routes import router
from app.database import init_db

app = FastAPI(
    title="Crypto Price Tracker API",
    description="API for tracking cryptocurrency prices from Deribit",
    version="1.0.0"
)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Crypto Price Tracker API is running"}
