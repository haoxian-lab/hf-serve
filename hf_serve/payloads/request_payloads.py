from typing import Any, Dict, List

from pydantic import BaseModel, Field


class TextPayload(BaseModel):
    data: str = Field()


class ImagePayload(BaseModel):
    data: bytes = Field()


# TODO: Add support for image URLs # pylint: disable=fixme
# class ImageUrlPayload(BaseModel):
#     data: str = Field()


class FeatureExtractionRequestPayload(BaseModel):
    data: str


class TextClassificationResponsePayload(BaseModel):
    results: List[Dict[str, Any]]
