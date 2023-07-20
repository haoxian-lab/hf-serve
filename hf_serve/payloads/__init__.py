from .request_payloads import *
from .response_payloads import *

REQUEST_PAYLOADS = {
    "text-classification": TextPayload,
    "feature-extraction": FeatureExtractionRequestPayload,
}

RESPONSE_PAYLOADS = {
    "text-classification": TextClassificationResponsePayload,
    "feature-extraction": FeatureExtractionResponsePayload,
}
