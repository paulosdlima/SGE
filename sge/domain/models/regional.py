from typing import Optional
import uuid

from pydantic import BaseModel, Field


class Regional(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    name: str = Field()
    description: str = Field()


class UpdateRegional(BaseModel):
    name: Optional[str]
    description: Optional[str]
