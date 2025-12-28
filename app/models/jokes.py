from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class JokesOrm(Base):
    __tablename__ = 'jokes_orm'
    text: Mapped[str] = mapped_column(unique=True, nullable=False)
    count_likes: Mapped[int] = mapped_column(default=0, nullable=False)
    count_dislikes: Mapped[int] = mapped_column(default=0, nullable=False)