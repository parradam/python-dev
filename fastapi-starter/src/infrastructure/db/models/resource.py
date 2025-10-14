from sqlalchemy import Column, Integer, String

from src.infrastructure.db.models.base import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    link = Column(String)
    isbn = Column(String)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}"
