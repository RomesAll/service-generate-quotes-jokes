from app.models import JokesOrm
from sqlalchemy import select, text, desc
from app.core.exception_handler import RecordNotFoundError, DuplicateKeyError
from sqlalchemy.orm import Session
from app.core import settings

class JokesRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client = client

    def select_jokes_by_search(self, text_joke: str = None, count_likes: int = None, count_dislikes: int = None):
        query = None
        if text_joke:
            query = select(JokesOrm).filter(JokesOrm.text.contains(text_joke))
        if count_likes:
            query = query.filter(JokesOrm.count_likes == count_likes)
        if count_dislikes:
            query = query.filter(JokesOrm.count_dislikes == count_dislikes)
        records = self.session.execute(query)
        result = records.scalars().all()
        return result

    def select_most_popular_jokes(self, pagination):
        query = select(JokesOrm).order_by(desc(JokesOrm.count_likes)).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        return result

    def select_filter_jokes_by_year(self, year: int, pagination):
        query = select(JokesOrm).filter(JokesOrm.year == year).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        return result

    def select_all_jokes(self, pagination):
        query = select(JokesOrm).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_jokes_by_id(self, jokes_id: int):
        if not self.session.get(JokesOrm, {'id': int(jokes_id)}):
            raise RecordNotFoundError(message="jokes_id not found")
        orm_object = self.session.get(JokesOrm, {'id': int(jokes_id)})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def create_jokes(self, orm_object: JokesOrm):
        if self.session.execute(text("SELECT id FROM jokes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise DuplicateKeyError(message='text already exists')
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_jokes(self, orm_object: JokesOrm):
        updating_record = self.session.get(JokesOrm, {'id': int(orm_object.id)})
        if not updating_record:
            raise RecordNotFoundError(message="Jokes not found")
        if self.session.execute(text("SELECT id FROM jokes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise DuplicateKeyError(message='text already exists')
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_jokes(self, jokes_id: int):
        orm_object = self.session.get(JokesOrm, {'id': int(jokes_id)})
        if not orm_object:
            raise RecordNotFoundError(message="Jokes not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object