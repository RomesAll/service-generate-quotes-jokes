from pydantic import BaseModel, ConfigDict, Field, computed_field
from datetime import datetime

class JokesSchemaPOST(BaseModel):
    text: str = Field(default='def_text')
    count_likes: int = Field(default='def_count_likes')
    count_dislikes: int = Field(default='def_count_dislikes')
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def overall_assessment(self) -> int:
        return self.count_likes - self.count_dislikes

class JokesSchemaGET(JokesSchemaPOST):
    id: int
    created_at: datetime
    updated_ad: datetime

class JokesSchemaPUT(JokesSchemaPOST):
    id: int