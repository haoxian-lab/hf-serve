from typing import Any, Dict, List

from pydantic import BaseModel


class TextClassificationResponsePayload(BaseModel):
    result: List[Dict[str, Any]]


class FeatureExtractionResponsePayload(BaseModel):
    result: List[float]
