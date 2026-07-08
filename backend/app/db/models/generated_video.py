"""
Database model for generated videos.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class GeneratedVideo(Base):
    """Stores AI-generated videos for a project."""

    __tablename__ = "generated_videos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    video_url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    duration: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    resolution: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="generated_video",
    )