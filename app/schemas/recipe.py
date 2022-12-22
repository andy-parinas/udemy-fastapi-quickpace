from typing import Sequence
from pydantic import BaseModel, HttpUrl


class RecipeBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class RecipeCreate(RecipeBase):
    submitter_id: int


class RecipeUpdate(RecipeBase):
    pass


class RecipeInDbBase(RecipeBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True

class Recipe(RecipeInDbBase):
    pass


class RecipeInDb(RecipeInDbBase):
    pass

class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]