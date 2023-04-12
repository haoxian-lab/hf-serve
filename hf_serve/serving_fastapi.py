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

    response_q = asyncio.Queue()
    await app.model_queue.put((string, response_q))
    output = await response_q.get()
    response.status_code = 200
    return output


@app.on_event("startup")
async def startup_event():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(server_loop(q))


async def server_loop(q):
    pipe = pipeline(model=MODEL, top_k=None, device=DEVICE)
    while True:
        (string, response_q) = await q.get()
        out = pipe(string)
        await response_q.put(out)
