import asyncio

from fastapi import APIRouter, Response
from loguru import logger
from prometheus_client import Histogram
from starlette.requests import Request

from hf_serve.config import settings
from hf_serve.payloads import REQUEST_PAYLOADS, RESPONSE_PAYLOADS

router = APIRouter()

request_payload = REQUEST_PAYLOADS[settings.TASK]
response_payload = RESPONSE_PAYLOADS[settings.TASK]

latency_metric = Histogram(
    "request_latency_seconds",
    "Latency of requests",
    buckets=[0.001, 0.01, 0.1, 1, 10],
)


@router.post("/")
async def inference(
    request: Request, request_data: request_payload, response: Response
) -> response_payload:
    data = request_data.data
    logger.info(f"Received request of type: `{type(data)}`")
    response_q = asyncio.Queue()
    await request.app.model_queue.put((data, response_q))

    # Start measuring the request latency
    with latency_metric.time():
        output = await response_q.get()

    response.status_code = 200
    if isinstance(output, list) and isinstance(output[0], list):
        output = output[0][0]
    return {"result": output}
