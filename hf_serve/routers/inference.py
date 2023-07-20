import asyncio
from typing import Any, Dict, List

from fastapi import APIRouter, Response
from loguru import logger
from prometheus_client import Histogram
from starlette.requests import Request

from hf_serve.config import settings
from hf_serve.payloads import PAYLOADS

router = APIRouter()

payload = PAYLOADS[settings.TASK]

latency_metric = Histogram(
    "request_latency_seconds",
    "Latency of requests",
    buckets=[0.001, 0.01, 0.1, 1, 10],
)


@router.post("/")
async def inference(
    request: Request, data: payload, response: Response
) -> List[Dict[str, Any]]:
    string = data.text_data
    logger.info(f"Received request: `{string}`")
    response_q = asyncio.Queue()
    await request.app.model_queue.put((string, response_q))

    # Start measuring the request latency
    with latency_metric.time():
        output = await response_q.get()

    response.status_code = 200
    return output
