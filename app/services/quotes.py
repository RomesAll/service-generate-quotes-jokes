from app.models import QuotesOrm, AuthorOrm
from app.schemas import (QuotesSchemaGET, QuotesSchemaPOST,
                         QuotesSchemaPUT, AuthorSchemaGET, AuthorSchemaPOST, AuthorSchemaPUT, AuthorSchemaRel, QuotesSchemaRel)
from app.repository import QuotesRepository, AuthorRepository

class QuotesService:

    def __init__(self, session):
        self.session = session

    def select_all_quotes(self) -> list[QuotesSchemaGET]:
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session).select_all_quotes()
        dto_objects: list[QuotesSchemaGET] = [QuotesSchemaGET.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_all_quotes_rel(self) -> list[QuotesSchemaRel]:
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session).select_all_quotes_rel()
        dto_objects: list[QuotesSchemaRel] = [QuotesSchemaRel.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_quotes_by_id(self, quotes_id: int) -> QuotesSchemaGET:
        orm_object: QuotesOrm = QuotesRepository(session=self.session).select_quotes_by_id(quotes_id)
        dto_object: QuotesSchemaGET = QuotesSchemaGET.model_validate(orm_object)
        return dto_object

    def select_quotes_by_id_rel(self, quotes_id: int) -> QuotesSchemaRel:
        orm_object: QuotesOrm = QuotesRepository(session=self.session).select_quotes_by_id_rel(quotes_id)
        dto_object: QuotesSchemaRel = QuotesSchemaRel.model_validate(orm_object)
        return dto_object

    def create_quotes(self, dto_object: QuotesSchemaPOST) -> QuotesSchemaGET:
        orm_object = QuotesOrm(**dto_object.model_dump(exclude_none=True, exclude_computed_fields=True))
        result = QuotesRepository(session=self.session).create_quotes(orm_object)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        return dto_object_result

    def update_quotes(self, dto_object: QuotesSchemaPUT) -> QuotesSchemaGET:
        orm_object = QuotesOrm(**dto_object.model_dump(exclude_defaults=True))
        result = QuotesRepository(session=self.session).update_quotes(orm_object)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        return dto_object_result

    def delete_quotes(self, quotes_id: int) -> QuotesSchemaGET:
        result = QuotesRepository(session=self.session).delete_quotes(quotes_id)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        return dto_object_result

class AuthorService:

    def __init__(self, session):
        self.session = session

    def select_all_author(self) -> list[AuthorSchemaGET]:
        orm_objects: list[AuthorOrm] = AuthorRepository(session=self.session).select_all_author()
        dto_objects: list[AuthorSchemaGET] = [AuthorSchemaGET.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_all_author_rel(self) -> list[AuthorSchemaRel]:
        orm_objects: list[AuthorOrm] = AuthorRepository(session=self.session).select_all_author_rel()
        dto_objects: list[AuthorSchemaRel] = [AuthorSchemaRel.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_author_by_id(self, author_id: int) -> AuthorSchemaGET:
        orm_object: AuthorOrm = AuthorRepository(session=self.session).select_author_by_id(author_id)
        dto_object: AuthorSchemaGET = AuthorSchemaGET.model_validate(orm_object)
        return dto_object

    def select_author_by_id_rel(self, author_id: int) -> AuthorSchemaRel:
        orm_object: AuthorOrm = AuthorRepository(session=self.session).select_author_by_id_rel(author_id)
        dto_object: AuthorSchemaRel = AuthorSchemaRel.model_validate(orm_object)
        return dto_object

    def create_author(self, dto_object: AuthorSchemaPOST) -> AuthorSchemaGET:
        orm_object = AuthorOrm(**dto_object.model_dump(exclude_none=True))
        result = AuthorRepository(session=self.session).create_author(orm_object)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        return dto_object_result

    def update_author(self, dto_object: AuthorSchemaPUT) -> AuthorSchemaGET:
        orm_object = AuthorOrm(**dto_object.model_dump(exclude_defaults=True))
        result = AuthorRepository(session=self.session).update_author(orm_object)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        return dto_object_result

    def delete_author(self, quotes_id: int) -> AuthorSchemaGET:
        result = AuthorRepository(session=self.session).delete_author(quotes_id)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        return dto_object_result