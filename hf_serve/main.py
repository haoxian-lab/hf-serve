import asyncio
import shutil
from collections import deque
from contextlib import asynccontextmanager
from time import time

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from loguru import logger
from prometheus_client import Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from transformers import pipeline

from hf_serve.config import settings
from hf_serve.routers import api_router

pipe = None


@asynccontextmanager
async def lifespan(myapp: FastAPI):
    """
    This context manager is used to load the model before the server
    starts to receive requests
    """
    instrumentator.expose(app)
    global pipe  # pylint: disable=global-statement
    logger.info(f"Loading the model... Using device {settings.DEVICE}")
    pipe = pipeline(
        task=settings.TASK,
        model=settings.MODEL,
        device=settings.DEVICE,
        model_kwargs={"cache_dir": settings.MODEL_CACHE_DIR},
    )
    queue = asyncio.Queue()
    myapp.model_queue = queue
    asyncio.create_task(server_loop(queue))
    yield
    # Clean up model
    pipe = None
    if settings.CLEAR_MODEL_CACHE_ON_SHUTDOWN:
        logger.info("Clearing the model cache...")
        shutil.rmtree(settings.MODEL_CACHE_DIR)


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
instrumentator = Instrumentator().instrument(app)

# Create Prometheus Histogram metrics
inference_time_metric = Histogram(
    "model_inference_time_seconds",
    "Time taken for model inference",
    buckets=[0.001, 0.01, 0.1, 1, 10],
)


inference_latency_queue = deque(maxlen=10)


async def server_loop(model_queue: asyncio.Queue):
    logger.info("Loading the model...")
    logger.info(f"Using device: {settings.DEVICE}")

    while True:
        (data, response_q) = await model_queue.get()
        logger.info(f"Received request: `{data}`")
        datum = [data]
        queues = [response_q]
        for _ in range(10):  # 10 is the max batch size
            try:
                (data, response_q) = await asyncio.wait_for(
                    model_queue.get(), timeout=0.01
                )  # 100ms
                datum.append(data)
                queues.append(response_q)
            except asyncio.exceptions.TimeoutError:
                logger.info(f"Batching requests stopped..., batch size: {len(datum)}")
                break

        # Start measuring the model inference time
        begin_time = time()
        # pylint: disable=not-callable
        outs = pipe(datum, batch_size=len(datum), top_k=-1)
        duration = time() - begin_time
        inference_time_metric.observe(duration)
        inference_latency_queue.append(duration)
        for out, response_q in zip(outs, queues):
            # logger.debug(f"Sending response: `{out}`")
            await response_q.put(out)


@app.get("/healthz")
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


@app.get("/readyz")
def model_loaded() -> JSONResponse:
    if pipe is None:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "model not loaded"},
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"status": "model loaded"}
    )
