from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.elastic import es
from app.dependencies import get_db
from app.models import Document
from app.schemas import DocumentResponse
from app.services.elastic import search_documents

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/search", response_model=list[DocumentResponse])
async def search(q: str, db: AsyncSession = Depends(get_db)):
    ids = await search_documents(q)

    if not ids:
        return []

    result = await db.execute(
        select(Document).where(Document.id.in_(ids))
    )

    docs = result.scalars().all()

    docs_map = {doc.id: doc for doc in docs}

    ordered_docs = [
        docs_map[i] for i in ids if i in docs_map
    ]

    ordered_docs.sort(
        key=lambda x: x.created_date,
        reverse=True
    )

    return ordered_docs[:20]


@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Document).where(Document.id == doc_id)
    )

    doc = result.scalar_one_or_none()

    if not doc:
        return {"status": "not found"}

    await db.delete(doc)
    await db.commit()

    try:
        await es.delete(
            index="documents",
            id=doc_id
        )
    except Exception:
        pass

    return {"status": "deleted"}