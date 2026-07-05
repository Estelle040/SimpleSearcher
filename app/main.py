from fastapi import FastAPI

from app.database import engine, Base

app = FastAPI(
    title="Document Search API",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    # создаем таблицы при старте (для тестового ок)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Service is running"}