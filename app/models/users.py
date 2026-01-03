from sqlalchemy import func, Column
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

class UsersOrm(Base):
    __tablename__ = "users_orm"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes]
    active: Mapped[bool] = mapped_column(server_default='false', nullable=False)