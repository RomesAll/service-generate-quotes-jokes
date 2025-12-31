from app.models import AuthorOrm, QuotesOrm
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload, joinedload
from app.core.exception_handler import RecordNotFoundError, DuplicateKeyError
from sqlalchemy.orm import Session
from app.core import settings

class QuotesRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client = client

    def select_all_quotes(self):
        query = select(QuotesOrm)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_all_quotes_rel(self):
        query = select(QuotesOrm).options(joinedload(QuotesOrm.author))
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_quotes_by_id(self, quotes_id: int):
        if not self.session.get(QuotesOrm, {'id': int(quotes_id)}):
            raise RecordNotFoundError(message="quotes_id not found")
        orm_object = self.session.get(QuotesOrm, {'id': int(quotes_id)})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def select_quotes_by_id_rel(self, quotes_id: int):
        if not self.session.get(QuotesOrm, {'id': int(quotes_id)}):
            raise RecordNotFoundError(message="quotes_id not found")
        query = select(QuotesOrm).filter(QuotesOrm.id == int(quotes_id)).options(joinedload(QuotesOrm.author))
        record = self.session.execute(query)
        result = record.scalar()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def create_quotes(self, orm_object: QuotesOrm):
        if not self.session.get(AuthorOrm, {'id': int(orm_object.author_id)}):
            raise RecordNotFoundError(message="author_id not found")
        if self.session.execute(text("SELECT id FROM quotes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise DuplicateKeyError(message='text already exists')
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_quotes(self, orm_object: QuotesOrm):
        updating_record = self.session.get(QuotesOrm, {'id': int(orm_object.id)})
        if not updating_record:
            raise RecordNotFoundError(message="Quotes not found")
        if not self.session.get(AuthorOrm, {'id': int(orm_object.author_id)}):
            raise RecordNotFoundError(message="author_id not found")
        if self.session.execute(text("SELECT id FROM quotes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise DuplicateKeyError(message='text already exists')
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_quotes(self, quotes_id: int):
        orm_object = self.session.get(QuotesOrm, {'id': int(quotes_id)})
        if not orm_object:
            raise RecordNotFoundError(message="Quotes not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object

class AuthorRepository:

    def __init__(self, session, client):
        self.session = session
        self.client = None

    def select_all_author(self):
        query = select(AuthorOrm)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_all_author_rel(self):
        query = select(AuthorOrm).options(selectinload(AuthorOrm.quotes))
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_author_by_id(self, author_id: int):
        if not self.session.get(AuthorOrm, {'id': int(author_id)}):
            raise RecordNotFoundError(message="author_id not found")
        orm_object = self.session.get(AuthorOrm, {'id': int(author_id)})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def select_author_by_id_rel(self, author_id: int):
        query = select(AuthorOrm).filter(AuthorOrm.id == int(author_id)).options(selectinload(AuthorOrm.quotes))
        records = self.session.execute(query)
        result = records.scalar()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def create_author(self, orm_object: AuthorOrm):
        if self.session.execute(text("SELECT id FROM author_orm WHERE fio=:fio LIMIT 1"), {'fio': orm_object.fio}).scalar_one_or_none():
            raise DuplicateKeyError(message='fio already exists')
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_author(self, orm_object: AuthorOrm):
        updating_record = self.session.get(AuthorOrm, {'id': int(orm_object.id)})
        if not updating_record:
            raise RecordNotFoundError(message="Author not found")
        if self.session.execute(text("SELECT id FROM author_orm WHERE fio=:fio LIMIT 1"), {'fio': orm_object.fio}).scalar_one_or_none():
            raise DuplicateKeyError(message='fio already exists')
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_author(self, author_id: int):
        orm_object = self.session.get(AuthorOrm, {'id': int(author_id)})
        if not orm_object:
            raise RecordNotFoundError(message="Author not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object