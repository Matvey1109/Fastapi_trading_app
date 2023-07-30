from sqlalchemy import (
    String, TIMESTAMP,
    Column, Integer,
)
from src.database import Base


class Operation(Base):
    __tablename__ = "operation"

    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=True)
    date = Column(TIMESTAMP)
    type = Column(String)
