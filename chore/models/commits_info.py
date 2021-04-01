from sqlalchemy import Column, String, JSON

from .base import BaseModel


class DBAssemblyInformation(BaseModel):
    __tablename__ = 'assemblyinformation'

    author = Column(
        String,
        nullable=False
    )

    commit_message = Column(
        String,
        nullable=False
    )

    commit_id = Column(
        String,
        nullable=False
    )

    assembly = Column(
        JSON,
        nullable=False
    )

    date = Column(
        String,
        nullable=False
    )
