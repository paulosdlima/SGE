import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GenderEnum(str, Enum):
    M = 'M'
    F = 'F'


class Employee(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    area: uuid.UUID = Field()
    enrollment: int = Field()
    name: str = Field()
    gender: GenderEnum = Field()
    phone: str = Field()
    active: bool = Field(default=True)


class UpdateEmployee(BaseModel):
    enrollment: Optional[int]
    name: Optional[str]
    gender: Optional[GenderEnum]
    phone: Optional[str]
    active: Optional[bool]
