from typing import Optional
import uuid

from pydantic import BaseModel, Field


class Area(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    regional: uuid.UUID = Field()
    name: str = Field()
    description: str = Field()


class UpdateArea(BaseModel):
    name: Optional[str]
    description: Optional[str]
