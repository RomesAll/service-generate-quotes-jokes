from app.models import JokesOrm
from sqlalchemy import select

class JokesRepository:

    def __init__(self, session):
        self.session = session

    def select_all_jokes(self):
        query = select(JokesOrm)
        records = self.session.execute(query)
        return records.scalars().all()

    def select_jokes_by_id(self, jokes_id: int):
        orm_object = self.session.get(JokesOrm, {'id': int(jokes_id)})
        return orm_object

    def create_jokes(self, orm_object: JokesOrm):
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        return orm_object

    def update_jokes(self, orm_object: JokesOrm):
        updating_record = self.session.get(JokesOrm, {'id': int(orm_object.id)})
        if not updating_record:
            pass
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        return updating_record

    def delete_jokes(self, jokes_id: int):
        orm_object = self.session.get(JokesOrm, {'id': int(jokes_id)})
        if not orm_object:
            pass
        self.session.delete(orm_object)
        self.session.commit()
        return orm_object