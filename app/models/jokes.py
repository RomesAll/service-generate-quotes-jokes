from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID

class JokesOrm(Base):
    __tablename__ = 'jokes_orm'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    text: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    count_likes: Mapped[int] = mapped_column(default=0, nullable=False)
    count_dislikes: Mapped[int] = mapped_column(default=0, nullable=False)