from datetime import datetime
import uuid

from sqlalchemy import ForeignKey, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database.database import Base
from settings import AuthJWTSettings


class RefreshSessionModel(Base):
    __tablename__ = "refresh_session"

    id: Mapped[uuid.uuid4] = mapped_column(
        UUID(), primary_key=True, default=uuid.uuid4
    )
    token: Mapped[uuid.uuid4] = mapped_column(UUID)
    expire_time_seconds: Mapped[int] = mapped_column(
        default=AuthJWTSettings.REFRESH_TOKEN_EXPIRE_SECONDS
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    user_id: Mapped[uuid.uuid4] = mapped_column(
        UUID, ForeignKey("user.id", ondelete="CASCADE")
    )
