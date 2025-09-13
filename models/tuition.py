from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import datetime, date, timezone
from decimal import Decimal
from pydantic import BaseModel, Field, StringConstraints
from enum import Enum

from .person import UNIType

class TuitionType(str, Enum):
    TUITION = "tuition"
    LIBRARY_FEE = "library_fee"
    GYM_FEE = "gym_fee"

class Semester(str, Enum):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class TuitionBase(BaseModel):
    student_uni: UNIType = Field(
        ...,
        description="Columbia University UNI of the student.",
        json_schema_extra={"example": "vv2418"},
    )
    tuition_type: TuitionType = Field(
        ...,
        description="Type of tuition or fee.",
        json_schema_extra={"example": "tuition"},
    )
    semester: Semester = Field(
        ...,
        description="Academic semester.",
        json_schema_extra={"example": "Fall"},
    )
    year: int = Field(
        ...,
        description="Academic year.",
        json_schema_extra={"example": 2024},
    )
    amount: Decimal = Field(
        ...,
        decimal_places=2,
        description="Tuition amount.",
        json_schema_extra={"example": "25000.00"},
    )
    due_date: date = Field(
        ...,
        description="Payment due date.",
        json_schema_extra={"example": "2024-08-15"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "student_uni": "vv2418",
                    "tuition_type": "tuition",
                    "semester": "Fall",
                    "year": 2024,
                    "amount": "25000.00",
                    "due_date": "2024-08-15",
                }
            ]
        }
    }


class TuitionCreate(TuitionBase):
    """Creation payload for a Tuition record."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "student_uni": "xy123",
                    "tuition_type": "gym_fee",
                    "semester": "Spring",
                    "year": 2024,
                    "amount": "500.00",
                    "due_date": "2024-01-20",
                }
            ]
        }
    }


class TuitionUpdate(BaseModel):
    """Partial update for a Tuition record; supply only fields to change."""
    student_uni: Optional[UNIType] = Field(
        None,
        description="Columbia University UNI of the student.",
        json_schema_extra={"example": "xyz456"}
    )
    tuition_type: Optional[TuitionType] = Field(
        None,
        description="Type of tuition or fee.",
        json_schema_extra={"example": "gym_fee"}
    )
    semester: Optional[Semester] = Field(
        None,
        description="Academic semester.",
        json_schema_extra={"example": "Fall"}
    )
    year: Optional[int] = Field(
        None,
        description="Academic year.",
        json_schema_extra={"example": 2025}
    )
    amount: Optional[Decimal] = Field(
        None,
        decimal_places=2,
        description="Tuition amount.",
        json_schema_extra={"example": "36576.00"}
    )
    due_date: Optional[date] = Field(
        None,
        description="Payment due date.",
        json_schema_extra={"example": "2024-09-19"}
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"amount": "36576.00", "tuition_type": "gym_fee"},
            ]
        }
    }


class TuitionRead(TuitionBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Tuition ID.",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "student_uni": "vv2418",
                    "tuition_type": "gym_fee",
                    "semester": "Fall",
                    "year": 2024,
                    "amount": "25000.00",
                    "due_date": "2024-08-15",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
