from app.models import QuotesOrm, AuthorOrm
from app.schemas import (QuotesSchemaGET, QuotesSchemaPOST,
                         QuotesSchemaPUT, AuthorSchemaGET, AuthorSchemaPOST, AuthorSchemaPUT, AuthorSchemaRel, QuotesSchemaRel)
from app.repository import QuotesRepository, AuthorRepository
from app.core import settings
import uuid

class QuotesService:

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def select_random_quotes(self):
        orm_object: QuotesOrm = QuotesRepository(session=self.session, client=self.client).select_random_quotes()
        dto_object: QuotesSchemaRel = QuotesSchemaRel.model_validate(orm_object)
        return dto_object

    def select_quotes_by_search(self, text_quotes: str = None, count_likes: int = None, count_dislikes: int = None):
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session,client=self.client).select_quotes_by_search(text_quotes, count_likes, count_dislikes)
        dto_objects: list[QuotesSchemaRel] = [QuotesSchemaRel.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_most_popular_quotes(self, pagination):
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session, client=self.client).select_most_popular_quotes(pagination)
        dto_objects: list[QuotesSchemaRel] = [QuotesSchemaRel.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_filter_quotes_by_year(self, year: int, pagination):
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session, client=self.client).select_filter_quotes_by_year(year, pagination)
        dto_objects: list[QuotesSchemaGET] = [QuotesSchemaGET.model_validate(row) for row in orm_objects]
        return dto_objects

    def select_all_quotes(self, pagination) -> list[QuotesSchemaGET]:
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session, client=self.client).select_all_quotes(pagination)
        dto_objects: list[QuotesSchemaGET] = [QuotesSchemaGET.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_all_quotes_rel(self, pagination) -> list[QuotesSchemaRel]:
        orm_objects: list[QuotesOrm] = QuotesRepository(session=self.session, client=self.client).select_all_quotes_rel(pagination)
        dto_objects: list[QuotesSchemaRel] = [QuotesSchemaRel.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_quotes_by_id(self, quotes_id: uuid.UUID) -> QuotesSchemaGET:
        orm_object: QuotesOrm = QuotesRepository(session=self.session, client=self.client).select_quotes_by_id(quotes_id)
        dto_object: QuotesSchemaGET = QuotesSchemaGET.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def select_quotes_by_id_rel(self, quotes_id: uuid.UUID) -> QuotesSchemaRel:
        orm_object: QuotesOrm = QuotesRepository(session=self.session, client=self.client).select_quotes_by_id_rel(quotes_id)
        dto_object: QuotesSchemaRel = QuotesSchemaRel.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def create_quotes(self, dto_object: QuotesSchemaPOST) -> QuotesSchemaGET:
        orm_object = QuotesOrm(**dto_object.model_dump(exclude_none=True, exclude_computed_fields=True))
        result = QuotesRepository(session=self.session, client=self.client).create_quotes(orm_object)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def update_quotes(self, dto_object: QuotesSchemaPUT) -> QuotesSchemaGET:
        orm_object = QuotesOrm(**dto_object.model_dump(exclude_defaults=True))
        result = QuotesRepository(session=self.session, client=self.client).update_quotes(orm_object)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def delete_quotes(self, quotes_id: uuid.UUID) -> QuotesSchemaGET:
        result = QuotesRepository(session=self.session, client=self.client).delete_quotes(quotes_id)
        dto_object_result = QuotesSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

class AuthorService:

    def __init__(self, session, client):
        self.session = session
        self.client = client

    def select_all_author(self) -> list[AuthorSchemaGET]:
        orm_objects: list[AuthorOrm] = AuthorRepository(session=self.session, client=self.client).select_all_author()
        dto_objects: list[AuthorSchemaGET] = [AuthorSchemaGET.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_all_author_rel(self) -> list[AuthorSchemaRel]:
        orm_objects: list[AuthorOrm] = AuthorRepository(session=self.session, client=self.client).select_all_author_rel()
        dto_objects: list[AuthorSchemaRel] = [AuthorSchemaRel.model_validate(row) for row in orm_objects]
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_objects)
        return dto_objects

    def select_author_by_id(self, author_id: int) -> AuthorSchemaGET:
        orm_object: AuthorOrm = AuthorRepository(session=self.session, client=self.client).select_author_by_id(author_id)
        dto_object: AuthorSchemaGET = AuthorSchemaGET.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def select_author_by_id_rel(self, author_id: int) -> AuthorSchemaRel:
        orm_object: AuthorOrm = AuthorRepository(session=self.session, client=self.client).select_author_by_id_rel(author_id)
        dto_object: AuthorSchemaRel = AuthorSchemaRel.model_validate(orm_object)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object)
        return dto_object

    def create_author(self, dto_object: AuthorSchemaPOST) -> AuthorSchemaGET:
        orm_object = AuthorOrm(**dto_object.model_dump(exclude_none=True))
        result = AuthorRepository(session=self.session, client=self.client).create_author(orm_object)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def update_author(self, dto_object: AuthorSchemaPUT) -> AuthorSchemaGET:
        orm_object = AuthorOrm(**dto_object.model_dump(exclude_defaults=True))
        result = AuthorRepository(session=self.session, client=self.client).update_author(orm_object)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result

    def delete_author(self, author_id: int) -> AuthorSchemaGET:
        result = AuthorRepository(session=self.session, client=self.client).delete_author(author_id)
        dto_object_result = AuthorSchemaGET.model_validate(result)
        if settings.logger.isEnabledFor(10):
            settings.logger.debug("client: %s data from the "
                                  "database was converted to a dto model, data: %s", self.client, dto_object_result)
        return dto_object_result