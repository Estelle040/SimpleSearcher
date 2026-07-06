from elasticsearch import AsyncElasticsearch
import asyncio
from app.config import settings

es = AsyncElasticsearch(
    settings.ELASTIC_URL
)

async def wait_for_elasticsearch(retries: int = 30):
    """
    Ждет, пока Elasticsearch станет доступен.
    """
    for attempt in range(retries):
        try:
            if await es.ping():
                print("Elasticsearch connected")
                return True
        except Exception:
            pass

        print(f"Waiting for Elasticsearch... ({attempt + 1}/{retries})")
        await asyncio.sleep(2)

    return False

async def check_connection():
    return await es.ping()

async def create_index():
    exists = await es.indices.exists(index=settings.ELASTIC_INDEX)

    if not exists:
        await es.indices.create(
            index=settings.ELASTIC_INDEX,
            mappings={
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "text": {
                        "type": "text"
                    }
                }
            }
        )


async def index_document(document_id: int, text: str):
    await es.index(
        index=settings.ELASTIC_INDEX,
        id=document_id,
        document={
            "id": document_id,
            "text": text,
        },
    )


async def search_documents(query: str) -> list[int]:
    response = await es.search(
        index=settings.ELASTIC_INDEX,
        query={
            "match": {
                "text": query
            }
        },
        size=20,
    )

    return [
        int(hit["_source"]["id"])
        for hit in response["hits"]["hits"]
    ]