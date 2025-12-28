from app.models import JokesOrm
from app.schemas import JokesSchemaPOST, JokesSchemaPUT, JokesSchemaGET
from app.repository import JokesRepository

class JokesService:

    def __init__(self, session):
        self.session = session

    def select_all_jokes(self) -> list[JokesSchemaGET]:
        orm_objects: list[JokesOrm] = JokesRepository(session=self.session).select_all_jokes()
        dto_objects: list[JokesSchemaGET] = [JokesSchemaGET.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_jokes_by_id(self, jokes_id: int) -> JokesSchemaGET:
        orm_object: JokesOrm = JokesRepository(session=self.session).select_jokes_by_id(jokes_id)
        dto_object: JokesSchemaGET = JokesSchemaGET.model_validate(orm_object)
        return dto_object

    def create_jokes(self, dto_object: JokesSchemaPOST) -> JokesSchemaGET:
        orm_object = JokesOrm(**dto_object.model_dump(exclude_none=True, exclude_computed_fields=True))
        result = JokesRepository(session=self.session).create_jokes(orm_object)
        dto_object_result = JokesSchemaGET.model_validate(result)
        return dto_object_result

    def update_jokes(self, dto_object: JokesSchemaPUT) -> JokesSchemaGET:
        orm_object = JokesOrm(**dto_object.model_dump(exclude_defaults=True))
        result = JokesRepository(session=self.session).update_jokes(orm_object)
        dto_object_result = JokesSchemaGET.model_validate(result)
        return dto_object_result

    def delete_jokes(self, jokes_id: int) -> JokesSchemaGET:
        result = JokesRepository(session=self.session).delete_jokes(jokes_id)
        dto_object_result = JokesSchemaGET.model_validate(result)
        return dto_object_result