import uuid
from typing import Optional

from pydantic import BaseModel, Field


class EmployeeDetail(BaseModel):
    id: uuid.UUID
    leaves: Optional[list[dict]]
    mandatory_shifts: Optional[list[str]]
    free_days: Optional[int]


class ShiftSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias='_id')
    area: uuid.UUID
    year: int
    month: int
    employees: Optional[list[EmployeeDetail]]
