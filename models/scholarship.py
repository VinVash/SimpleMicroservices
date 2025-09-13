from __future__ import annotations

from typing import Optional, Annotated
from uuid import UUID, uuid4
from datetime import datetime, date, timezone
from decimal import Decimal
from pydantic import BaseModel, Field, StringConstraints
from enum import Enum

from .person import UNIType

class ScholarshipType(str, Enum):
    ACADEMIC_MERIT = "academic_merit"
    NEED_BASED = "need_based"
    RESEARCH = "research"
    DEPARTMENTAL = "departmental"

class ScholarshipStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AwardFrequency(str, Enum):
    ONE_TIME = "one_time"
    SEMESTER = "semester"
    ANNUAL = "annual"

class ScholarshipBase(BaseModel):
    name: str = Field(
        ...,
        description="Scholarship name or title.",
        json_schema_extra={"example": "Dean's Academic Excellence Scholarship"},
    )
    scholarship_type: ScholarshipType = Field(
        ...,
        description="Type/category of scholarship.",
        json_schema_extra={"example": "academic_merit"},
    )
    sponsor_organization: str = Field(
        ...,
        description="Organization or department sponsoring the scholarship.",
        json_schema_extra={"example": "Columbia University Engineering School"},
    )
    amount: Decimal = Field(
        ...,
        decimal_places=2,
        description="Scholarship amount per award period.",
        json_schema_extra={"example": "5000.00"},
    )
    is_active: bool = Field(
        default=True,
        description="Whether the scholarship is currently active and accepting applications.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Dean's Academic Excellence Scholarship",
                    "scholarship_type": "academic_merit",
                    "sponsor_organization": "Columbia University Engineering School",
                    "amount": "5000.00",
                    "is_active": True,
                }
            ]
        }
    }


class ScholarshipCreate(ScholarshipBase):
    """Creation payload for a Scholarship."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "International Student Support Grant",
                    "scholarship_type": "need_based",
                    "sponsor_organization": "Columbia Global Programs",
                    "amount": "3000.00",
                    "is_active": True,
                }
            ]
        }
    }


class ScholarshipUpdate(BaseModel):
    """Partial update for a Scholarship; supply only fields to change."""
    name: Optional[str] = Field(
        None,
        description="Scholarship name or title.",
        json_schema_extra={"example": "Updated Scholarship Name"}
    )
    scholarship_type: Optional[ScholarshipType] = Field(
        None,
        description="Type/category of scholarship.",
        json_schema_extra={"example": "need_based"}
    )
    sponsor_organization: Optional[str] = Field(
        None,
        description="Organization or department sponsoring the scholarship.",
        json_schema_extra={"example": "Alumni Association"}
    )
    amount: Optional[Decimal] = Field(
        None,
        decimal_places=2,
        description="Scholarship amount per award period.",
        json_schema_extra={"example": "6000.00"}
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the scholarship is currently active and accepting applications.",
        json_schema_extra={"example": False}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"amount": "6000.00", "sponsor_organization": "Alumni Association"},
                {"is_active": False, "sponsor_organization": "Alumni Association"},
            ]
        }
    }


class ScholarshipRead(ScholarshipBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Scholarship ID.",
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
                    "name": "Dean's Academic Excellence Scholarship",
                    "scholarship_type": "academic_merit",
                    "sponsor_organization": "Columbia University Engineering School",
                    "amount": "5000.00",
                    "is_active": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


