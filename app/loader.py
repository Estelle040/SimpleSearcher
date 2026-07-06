import ast
from datetime import datetime

import pandas as pd
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Document
from app.services.elastic import index_document

async def load_csv(path: str):
    df = pd.read_csv(path)

    async with AsyncSessionLocal() as session:

        for _, row in df.iterrows():

            existing = await session.execute(
                select(Document).where(
                    Document.text == row["text"]
                )
            )

            if existing.scalar():
                continue

            document = Document(
                text=row["text"],
                created_date=datetime.fromisoformat(
                    row["created_date"]
                ),
                rubrics=ast.literal_eval(
                    row["rubrics"]
                ),
            )

            session.add(document)

            await session.flush()

            await index_document(
                document.id,
                document.text
            )

        await session.commit()