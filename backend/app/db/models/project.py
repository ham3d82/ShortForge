"""
Project database model.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Project(Base):
    """Represents a generated AI project."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    tone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    hook: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    script: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hashtags: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    thumbnail_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    image_prompts: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )