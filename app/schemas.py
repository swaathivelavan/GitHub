from pydantic import BaseModel, Field
from typing import Optional, List


class Repository(BaseModel):
    repository_name: str
    repo_link: str


class RepositoryCollection(BaseModel):
    repositories: List[Repository]

