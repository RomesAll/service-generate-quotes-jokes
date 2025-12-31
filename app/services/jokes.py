from app.models import JokesOrm
from app.schemas import JokesSchemaPOST, JokesSchemaPUT, JokesSchemaGET
from app.repository import JokesRepository
from app.core import settings

class JokesService:

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def select_all_jokes(self) -> list[JokesSchemaGET]:
        orm_objects: list[JokesOrm] = JokesRepository(session=self.session, client=self.client).select_all_jokes()
        dto_objects: list[JokesSchemaGET] = [JokesSchemaGET.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_jokes_by_id(self, jokes_id: int) -> JokesSchemaGET:
        orm_object: JokesOrm = JokesRepository(session=self.session, client=self.client).select_jokes_by_id(jokes_id)
        dto_object: JokesSchemaGET = JokesSchemaGET.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def create_jokes(self, dto_object: JokesSchemaPOST) -> JokesSchemaGET:
        orm_object = JokesOrm(**dto_object.model_dump(exclude_none=True, exclude_computed_fields=True))
        result = JokesRepository(session=self.session, client=self.client).create_jokes(orm_object)
        dto_object_result = JokesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def update_jokes(self, dto_object: JokesSchemaPUT) -> JokesSchemaGET:
        orm_object = JokesOrm(**dto_object.model_dump(exclude_defaults=True))
        result = JokesRepository(session=self.session, client=self.client).update_jokes(orm_object)
        dto_object_result = JokesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def delete_jokes(self, jokes_id: int) -> JokesSchemaGET:
        result = JokesRepository(session=self.session, client=self.client).delete_jokes(jokes_id)
        dto_object_result = JokesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result