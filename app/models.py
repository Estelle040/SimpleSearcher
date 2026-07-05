from sqlalchemy import Column, Integer, Text, DateTime, JSON
from datetime import datetime

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    rubrics = Column(JSON, nullable=False)
    text = Column(Text, nullable=False)

    created_date = Column(DateTime, default=datetime.utcnow)