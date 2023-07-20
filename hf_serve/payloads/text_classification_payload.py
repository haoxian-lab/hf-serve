from typing import Any, Dict, List

from pydantic import BaseModel, Field


class TextClassificationRequestPayload(BaseModel):
    text_data: str = Field(
        default="A string to be classified", example="A string to be classified"
    )


class TextClassificationResponsePayload(BaseModel):
    results: List[Dict[str, Any]] = Field()
