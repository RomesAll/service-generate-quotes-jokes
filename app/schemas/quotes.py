from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import datetime
import uuid

class QuotesSchemaPOST(BaseModel):
    text: str = Field(default='def_text', min_length=5, max_length=100, examples=['ha-ha-ha'], description='Текст цитаты')
    year: int = Field(default='def_count_likes', ge=0, le=2050, examples=['2001'], description='Год написания шутки')
    author_id: int
    count_likes: int = Field(default='def_count_likes', ge=0, le=1000, examples=['0'], description='Кол-во лайков')
    count_dislikes: int = Field(default='def_count_dislikes', ge=0, le=1000, examples=['0'], description='Кол-во дизлайков')
    model_config = ConfigDict(from_attributes=True)

class QuotesSchemaGET(QuotesSchemaPOST):
    id: uuid.UUID
    created_at: datetime
    updated_ad: datetime

class QuotesSchemaPUT(QuotesSchemaPOST):
    id: uuid.UUID

class QuotesSchemaRel(QuotesSchemaGET):
    author: "AuthorSchemaGET"

class AuthorSchemaPOST(BaseModel):
    fio: str = Field(default='def_fio', min_length=5, max_length=100, examples=['Петров В.В.'])
    model_config = ConfigDict(from_attributes=True)

class AuthorSchemaGET(AuthorSchemaPOST):
    id: int
    created_at: datetime
    updated_ad: datetime

class AuthorSchemaPUT(AuthorSchemaPOST):
    id: int

class AuthorSchemaRel(AuthorSchemaGET):
    quotes: list["QuotesSchemaGET"]