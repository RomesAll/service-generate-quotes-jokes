from pydantic import BaseModel, Field

class SearchJokesSchema(BaseModel):
    text: str | None = Field(default=None)
    count_likes: int | None = Field(default=None, ge=0)
    count_dislikes: int | None = Field(default=None, ge=0)

class PaginationJokesSchema(BaseModel):
    limit: int = Field(default=20, ge=0, le=100, description='Кол-во записей')
    offset: int = Field(default=0, ge=0, description='Пропустить')