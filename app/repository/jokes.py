from fastapi import status
from fastapi.exceptions import HTTPException
from app.models import JokesOrm
from app.core import settings
from sqlalchemy.orm import Session
from sqlalchemy import select, text, desc
import random
import uuid

class JokesRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client = client

    def check_exist_pk(self, pk: uuid.UUID):
        query = select(JokesOrm).filter(JokesOrm.id == pk)
        records = self.session.execute(query)
        return records.scalar_one_or_none()

    def select_random_jokes(self):
        query = select(JokesOrm.id).select_from(JokesOrm)
        all_id = self.session.execute(query).scalars().all()
        if not all_id:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                detail='The database with jokes is empty, so it is impossible to display a random entry')
        random_object = self.session.get(JokesOrm, {'id': random.choice(all_id)})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, random_object)
        return random_object

    def select_jokes_by_search(self, text_joke: str = None, count_likes: int = None, count_dislikes: int = None):
        query = select(JokesOrm)
        if text_joke:
            query = query.filter(JokesOrm.text.contains(text_joke))
        if count_likes:
            query = query.filter(JokesOrm.count_likes == count_likes)
        if count_dislikes:
            query = query.filter(JokesOrm.count_dislikes == count_dislikes)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_most_popular_jokes(self, pagination):
        query = select(JokesOrm).order_by(desc(JokesOrm.count_likes)).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_filter_jokes_by_year(self, year: int, pagination):
        query = select(JokesOrm).filter(JokesOrm.year == year).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_all_jokes(self, pagination):
        query = select(JokesOrm).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_jokes_by_id(self, jokes_id: uuid.UUID):
        orm_object = self.session.get(JokesOrm, {'id': jokes_id})
        if not orm_object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found")
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def create_jokes(self, orm_object: JokesOrm):
        pk = uuid.uuid4()
        if self.session.execute(text("SELECT id FROM jokes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This text joke already exists')
        if self.check_exist_pk(pk):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Id joke already exists')
        orm_object.id = pk
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_jokes(self, orm_object: JokesOrm):
        updating_record = self.session.get(JokesOrm, {'id': orm_object.id})
        if not updating_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found")
        if self.session.execute(text("SELECT id FROM jokes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This text joke already exists')
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_jokes(self, jokes_id: uuid.UUID):
        orm_object = self.session.get(JokesOrm, {'id': jokes_id})
        if not orm_object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jokes not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object