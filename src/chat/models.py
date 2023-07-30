from sqlalchemy import (
    Column, Integer,
    String
)
from src.database import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    message = Column(String)
