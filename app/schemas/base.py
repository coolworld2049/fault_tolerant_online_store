from typing import Optional

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    id: Optional[int] = Field(
        sa_column=Column("id", Integer, primary_key=True, autoincrement=True)
    )
    model_config = ConfigDict(
        alias_generator=to_camel, arbitrary_types_allowed=True, populate_by_name=True
    )
