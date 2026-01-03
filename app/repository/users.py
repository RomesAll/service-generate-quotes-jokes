from app.models import UsersOrm
from sqlalchemy import select
from app.core.exception_handler import RecordNotFoundError, DuplicateKeyError
from app.core import settings
import uuid
from app.core.utils import hash_password

class UsersRepository:

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def check_exist_pk(self, pk: uuid.UUID):
        query = select(UsersOrm).filter(UsersOrm.id == pk)
        records = self.session.execute(query)
        return records.scalar_one_or_none()

    def select_all_users(self):
        query = select(UsersOrm)
        records = self.session.execute(query)
        result = records.scalars().all()
        return result

    def select_users_by_id(self, user_id: uuid.UUID):
        if not self.session.get(UsersOrm, {'id': user_id}):
            raise RecordNotFoundError(message="user_id not found")
        orm_object = self.session.get(UsersOrm, {'id': user_id})
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s has entered the data: %s", self.client, orm_object)
        return orm_object

    def select_users_by_username(self, username: str):
        query = select(UsersOrm).filter(UsersOrm.username == username)
        records = self.session.execute(query)
        result = records.scalar_one_or_none()
        return result

    def create_users(self, orm_object: UsersOrm):
        pk = uuid.uuid4()
        if self.check_exist_pk(pk):
            raise DuplicateKeyError(message='pk already exists')
        orm_object.id = pk
        orm_object.password = hash_password(orm_object.password.decode())
        self.session.add(orm_object)
        self.session.flush()
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s added the data: %s", self.client, orm_object)
        return orm_object

    def update_users(self, orm_object: UsersOrm):
        updating_record = self.session.get(UsersOrm, {'id': orm_object.id})
        if not updating_record:
            raise RecordNotFoundError(message="User not found")
        for key in orm_object.__table__.columns.keys():
            value = orm_object.__dict__.get(key, None)
            if value:
                setattr(updating_record, key, value)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s updated the data: %s", self.client, updating_record)
        return updating_record

    def delete_users(self, users_id: uuid.UUID):
        orm_object = self.session.get(UsersOrm, {'id': users_id})
        if not orm_object:
            raise RecordNotFoundError(message="User not found")
        self.session.delete(orm_object)
        self.session.commit()
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s deleted the data: %s", self.client, orm_object)
        return orm_object