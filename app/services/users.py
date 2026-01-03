from app.repository import UsersRepository, UsersOrm
from app.schemas import UsersSchemaPOST, UsersSchemaGET, UsersSchemaPUT
from app.core import settings
import uuid

class UsersService:

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def select_all_users(self):
        orm_objects = UsersRepository(session=self.session, client=self.client).select_all_users()
        dto_objects = [UsersSchemaGET.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_users_by_id(self, users_id: uuid.UUID):
        orm_object = UsersRepository(session=self.session, client=self.client).select_users_by_id(users_id)
        dto_object = UsersSchemaGET.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def create_users(self, dto_object: UsersSchemaPOST):
        orm_object = UsersOrm(**dto_object.model_dump(exclude_none=True))
        result = UsersRepository(session=self.session, client=self.client).create_users(orm_object)
        dto_object_result = UsersSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def update_users(self, dto_object: UsersSchemaPUT):
        orm_object = UsersOrm(**dto_object.model_dump(exclude_defaults=True))
        result = UsersRepository(session=self.session, client=self.client).update_users(orm_object)
        dto_object_result = UsersSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def delete_users(self, user_id: uuid.UUID):
        result = UsersRepository(session=self.session, client=self.client).delete_users(user_id)
        dto_object_result = UsersSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result