import aioredis
from fastapi import FastAPI
from fastapi import Request, Response
from transformers import pipeline
import asyncio
from hf_serve.config import DEVICE, MODEL

app = FastAPI()


@app.post("/")
async def homepage(request: Request, response: Response):
    payload = await request.body()
    # print(f"Received request: {payload}")
    string = payload.decode("utf-8")

    redis_conn = await app.redis_pool.acquire()
    response_q = asyncio.Queue()
    await redis_conn.rpush("requests_queue", string)
    await redis_conn.rpush("response_queue", await response_q.put())
    await app.redis_pool.release(redis_conn)
    output = await response_q.get()
    response.status_code = 200
    return output


async def server_loop():
    pipe = pipeline(model=MODEL, top_k=None, device=DEVICE)
    redis_conn = await app.redis_pool.acquire()
    while True:
        string = await redis_conn.lpop("requests_queue")
        if string is None:
            await asyncio.sleep(0.1)
            continue
        response_q_id = await redis_conn.lpop("response_queue")
        response_q = asyncio.Queue()
        app.redis_response_queues[response_q_id] = response_q
        out = pipe(string)
        response_q_id = response_q_id.decode("utf-8")
        await redis_conn.rpush(response_q_id, out)
        del app.redis_response_queues[response_q_id]
    await app.redis_pool.release(redis_conn)


@app.on_event("startup")
async def startup_event():
    app.redis_pool = await aioredis.create_redis_pool("redis://localhost")
    app.redis_response_queues = {}
    asyncio.create_task(server_loop())


@app.on_event("shutdown")
async def shutdown_event():
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
