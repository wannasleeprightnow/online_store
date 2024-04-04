import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
