from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class JokesSchemaPOST(BaseModel):
    text: str = Field(default='def_text', min_length=5, max_length=100, examples=['ha-ha-ha'], description='Текст шутки')
    year: int = Field(default='def_count_likes', ge=0, le=2050, examples=['2001'], description='Год написания шутки')
    count_likes: int = Field(default='def_count_likes', ge=0, le=1000, examples=['0'], description='Кол-во лайков')
    count_dislikes: int = Field(default='def_count_dislikes', ge=0, le=1000, examples=['0'], description='Кол-во дизлайков')
    model_config = ConfigDict(from_attributes=True)

class JokesSchemaGET(JokesSchemaPOST):
    id: uuid.UUID
    created_at: datetime
    updated_ad: datetime

class JokesSchemaPUT(JokesSchemaPOST):
    id: uuid.UUID