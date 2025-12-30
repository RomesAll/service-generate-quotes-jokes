from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from app.core import settings
from datetime import datetime, timezone

engine = create_engine(url=settings.postgresql.get_database_url_sync, echo=True)
session_maker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)

def get_current_time() -> datetime:
    dt = datetime.now(tz=timezone.utc)
    return dt

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_ad: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=get_current_time)
