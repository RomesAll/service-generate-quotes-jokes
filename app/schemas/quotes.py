from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import datetime

class QuotesSchemaPOST(BaseModel):
    text: str = Field(default='def_text', min_length=10, max_length=100, examples=['ha-ha-ha'], description='Текст цитаты')
    author_id: int
    count_likes: int = Field(default='def_count_likes', ge=0, le=1000, examples=['0'], description='Кол-во лайков')
    count_dislikes: int = Field(default='def_count_dislikes', ge=0, le=1000, examples=['0'], description='Кол-во дизлайков')
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def overall_assessment(self) -> int:
        return self.count_likes - self.count_dislikes

class QuotesSchemaGET(QuotesSchemaPOST):
    id: int
    created_at: datetime
    updated_ad: datetime

class QuotesSchemaPUT(QuotesSchemaPOST):
    id: int

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