from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    id: str
    content: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

class Chunk(BaseModel):

    id: str
    document_id: str
    content: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)