from app.models import AuthorOrm, QuotesOrm
from sqlalchemy import select, text, desc
from sqlalchemy.orm import selectinload, joinedload
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from app.core import settings
import random
import uuid

class QuotesRepository:

    def __init__(self, session, client):
        self.session: Session = session
        self.client = client

    def check_exist_pk(self, pk: uuid.UUID):
        query = select(QuotesOrm).filter(QuotesOrm.id == pk)
        records = self.session.execute(query)
        return records.scalar_one_or_none()

    def select_random_quotes(self):
        query = select(QuotesOrm.id).select_from(QuotesOrm)
        all_id = self.session.execute(query).scalars().all()
        if not all_id:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                detail='The database with quotes is empty, so it is impossible to display a random entry')
        random_object = self.session.get(QuotesOrm, {'id': random.choice(all_id)})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, random_object)
        return  random_object

    def select_quotes_by_search(self, text_quotes: str = None, count_likes: int = None, count_dislikes: int = None):
        query = select(QuotesOrm).options(joinedload(QuotesOrm.author))
        if text_quotes:
            query = query.filter(QuotesOrm.text.contains(text_quotes))
        if count_likes:
            query = query.filter(QuotesOrm.count_likes == count_likes)
        if count_dislikes:
            query = query.filter(QuotesOrm.count_dislikes == count_dislikes)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_most_popular_quotes(self, pagination):
        query = (select(QuotesOrm).options(joinedload(QuotesOrm.author)).
                 order_by(desc(QuotesOrm.count_likes)).limit(pagination.limit).offset(pagination.offset))
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_filter_quotes_by_year(self, year: int, pagination):
        query = select(QuotesOrm).filter(QuotesOrm.year == year).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_all_quotes(self, pagination):
        query = select(QuotesOrm).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_all_quotes_rel(self, pagination):
        query = select(QuotesOrm).options(joinedload(QuotesOrm.author)).limit(pagination.limit).offset(pagination.offset)
        records = self.session.execute(query)
        result = records.scalars().all()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def select_quotes_by_id(self, quotes_id: uuid.UUID):
        orm_object = self.session.get(QuotesOrm, {'id': quotes_id})
        if not orm_object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def select_quotes_by_id_rel(self, quotes_id: uuid.UUID):
        query = select(QuotesOrm).filter(QuotesOrm.id == quotes_id).options(joinedload(QuotesOrm.author))
        record = self.session.execute(query)
        result = record.scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def create_quotes(self, orm_object: QuotesOrm):
        pk = uuid.uuid4()
        if not self.session.get(AuthorOrm, {'id': int(orm_object.author_id)}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id author not found")
        if self.session.execute(text("SELECT id FROM quotes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This text quote already exists')
        if self.check_exist_pk(pk):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Id quote already exists')
        orm_object.id = pk
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_quotes(self, orm_object: QuotesOrm):
        updating_record = self.session.get(QuotesOrm, {'id': orm_object.id})
        if not updating_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
        if not self.session.get(AuthorOrm, {'id': int(orm_object.author_id)}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id author not found")
        if self.session.execute(text("SELECT id FROM quotes_orm WHERE text=:text LIMIT 1"), {'text': orm_object.text}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This text quote already exists')
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_quotes(self, quotes_id: uuid.UUID):
        orm_object = self.session.get(QuotesOrm, {'id': quotes_id})
        if not orm_object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object

class AuthorRepository:

    def __init__(self, session, client):
        self.session = session
        self.client = client

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
        orm_object = self.session.get(AuthorOrm, {'id': int(author_id)})
        if not orm_object:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def select_author_by_id_rel(self, author_id: int):
        query = select(AuthorOrm).filter(AuthorOrm.id == int(author_id)).options(selectinload(AuthorOrm.quotes))
        records = self.session.execute(query)
        result = records.scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, result)
        return result

    def create_author(self, orm_object: AuthorOrm):
        if self.session.execute(text("SELECT id FROM author_orm WHERE fio=:fio LIMIT 1"), {'fio': orm_object.fio}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This fio already exists')
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_author(self, orm_object: AuthorOrm):
        updating_record = self.session.get(AuthorOrm, {'id': int(orm_object.id)})
        if not updating_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
        if self.session.execute(text("SELECT id FROM author_orm WHERE fio=:fio LIMIT 1"), {'fio': orm_object.fio}).scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail='This fio already exists')
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Author not found')
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object