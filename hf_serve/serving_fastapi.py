import asyncio
from collections import deque
from functools import lru_cache
from time import time

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger
from prometheus_client import Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from transformers import pipeline

from hf_serve.config import DEVICE, MODEL

app = FastAPI()

# Create Prometheus Histogram metrics
inference_time_metric = Histogram(
    "model_inference_time_seconds",
    "Time taken for model inference",
    buckets=[0.001, 0.01, 0.1, 1, 10],
)
latency_metric = Histogram(
    "request_latency_seconds",
    "Latency of requests",
    buckets=[0.001, 0.01, 0.1, 1, 10],
)

inference_latency_queue = deque(maxlen=10)


@app.post("/")
async def homepage(request: Request, response: Response):
    payload = await request.body()
    # print(f"Received request: {payload}")
    string = payload.decode("utf-8")
    logger.info(f"Received request: `{string}`")
    response_q = asyncio.Queue()
    await app.model_queue.put((string, response_q))

    # Start measuring the request latency
    with latency_metric.time():
        output = await response_q.get()
    response.status_code = 200
    return output


@lru_cache(maxsize=128)  # Cache up to 128 most recently used results
def perform_inference(pipe, string):
    out = pipe(string)
    return out


@app.on_event("startup")
async def startup_event():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(server_loop(q))


async def server_loop(q):
    logger.info("Loading the model...")
    logger.info(f"Using device: {DEVICE}")
    pipe = pipeline(model=MODEL, top_k=None, device=DEVICE)
    while True:
        (string, response_q) = await q.get()

        # Start measuring the model inference time
        begin_time = time()
        out = perform_inference(pipe, string)
        duration = time() - begin_time
        inference_time_metric.observe(duration)
        inference_latency_queue.append(duration)

        await response_q.put(out)


@app.get("/health")
async def health_check():
    if len(inference_latency_queue) > 0:
        average_latency = sum(inference_latency_queue) / len(inference_latency_queue)
        threshold = 10  # seconds
        if average_latency > threshold:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "status": f"unhealthy with latency {average_latency} > {threshold}"
                },
            )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "healthy"})


if __name__ == "__main__":
    import uvicorn

    # Instrument the FastAPI application with Prometheus metrics
    Instrumentator().instrument(app).expose(app)
    logger.info("Starting the service...")

    uvicorn.run(app, host="0.0.0.0", port=8000)
