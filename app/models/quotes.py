from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database import Base

class AuthorOrm(Base):
    __tablename__ = 'author_orm'
    fio: Mapped[str] = mapped_column(default='Unknown', nullable=False, unique=True)
    quotes: Mapped[list["QuotesOrm"]] = relationship(back_populates="author")

class QuotesOrm(Base):
    __tablename__ = 'quotes_orm'
    text: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('author_orm.id', ondelete='CASCADE'), nullable=True)
    count_likes: Mapped[int] = mapped_column(default=0, nullable=False)
    count_dislikes: Mapped[int] = mapped_column(default=0, nullable=False)
    author: Mapped["AuthorOrm"] = relationship(back_populates='quotes')