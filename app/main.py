from contextlib import asynccontextmanager
from app.routers.admin import router as admin_router
from fastapi import FastAPI
from app.services.elastic import wait_for_elasticsearch
from app.database import Base, engine
from app.services.elastic import create_index, check_connection
from app.routers.documents import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        connected = await wait_for_elasticsearch()

        if connected:
            print("Elasticsearch connected")
            await create_index()
        else:
            print("Elasticsearch ping failed")

    except Exception as e:
        print(f"Elasticsearch error: {e}")

    yield

app = FastAPI(
    title="Document Search API",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return {"message": "Service is running"}

app.include_router(admin_router)
app.include_router(documents_router)