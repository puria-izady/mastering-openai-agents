from __future__ import annotations

from pydantic import BaseModel, Field


class CalendarEvent(BaseModel):
    title: str
    date: str
    attendees: list[str] = Field(default_factory=list)
    location: str | None = None


class DomainCheck(BaseModel):
    allowed: bool
    reason: str

