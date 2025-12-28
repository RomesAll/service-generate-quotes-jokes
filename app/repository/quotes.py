from app.models import AuthorOrm, QuotesOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

class QuotesRepository:

    def __init__(self, session):
        self.session = session

    def select_all_quotes(self):
        query = select(QuotesOrm)
        records = self.session.execute(query)
        return records.scalars().all()

    def select_all_quotes_rel(self):
        query = select(QuotesOrm).options(joinedload(QuotesOrm.author))
        records = self.session.execute(query)
        return records.scalars().all()

    def select_quotes_by_id(self, quotes_id: int):
        orm_object = self.session.get(QuotesOrm, {'id': int(quotes_id)})
        return orm_object

    def select_quotes_by_id_rel(self, author_id: int):
        query = select(QuotesOrm).filter(QuotesOrm.id == int(author_id)).options(joinedload(QuotesOrm.author))
        record = self.session.execute(query)
        return record.scalar()

    def create_quotes(self, orm_object: QuotesOrm):
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        return orm_object

    def update_quotes(self, orm_object: QuotesOrm):
        updating_record = self.session.get(QuotesOrm, {'id': int(orm_object.id)})
        if not updating_record:
            pass
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        return updating_record

    def delete_quotes(self, quotes_id: int):
        orm_object = self.session.get(QuotesOrm, {'id': int(quotes_id)})
        if not orm_object:
            pass
        self.session.delete(orm_object)
        self.session.commit()
        return quotes_id

class AuthorRepository:

    def __init__(self, session):
        self.session = session

    def select_all_author(self):
        query = select(AuthorOrm)
        records = self.session.execute(query)
        return records.scalars().all()

    def select_all_author_rel(self):
        query = select(AuthorOrm).options(selectinload(AuthorOrm.quotes))
        records = self.session.execute(query)
        return records.scalars().all()

    def select_author_by_id(self, author_id: int):
        orm_object = self.session.get(AuthorOrm, {'id': int(author_id)})
        return orm_object

    def select_author_by_id_rel(self, author_id: int):
        query = select(AuthorOrm).filter(AuthorOrm.id == int(author_id)).options(selectinload(AuthorOrm.quotes))
        records = self.session.execute(query)
        return records.scalar()

    def create_author(self, orm_object: AuthorOrm):
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        return orm_object

    def update_author(self, orm_object: AuthorOrm):
        updating_record = self.session.get(AuthorOrm, {'id': int(orm_object.id)})
        if not updating_record:
            pass
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        return updating_record

    def delete_author(self, author_id: int):
        orm_object = self.session.get(AuthorOrm, {'id': int(author_id)})
        if not orm_object:
            pass
        self.session.delete(orm_object)
        self.session.commit()
        return author_id