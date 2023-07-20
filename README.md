# hf-serve
Huggingface models serving with FastAPI

## Installation

### Use pip 
```bash
git clone https://github.com/haoxian-lab/hf-serve.git
cd hf-serve
pip install .
```

### Use docker
```bash
docker pull sharockys/hf-serve
docker run -p 8000:8000 sharockys/hf-serve
```

## Test 
```bash
curl -X POST "http://localhost:8000/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"data\":\"I love you\"}"
```

## Configuration 

### Environment variables
- `HF_SERVE_MODEL_NAME`: model name in huggingface model hub
- `HF_SERVE_TASK`: task name, one of `text-classification`, `feature-extraction`
- `HF_SERVE_USE_GPU`: whether to use gpu, default `False`
- `HF_SERVE_DEVICE`: device name, default `cpu`. For Mac OS use `mps`, for Nvidia GPU use `cuda`. Automatically if not specified.
- `HF_SERVE_MODEL_CACHE_DIR`: model cache dir, default `/tmp/hf-serve`
- `HF_SERVE_CLEAR_MODEL_CACHE_ON_SHUTDOWN`: whether to clear model cache on shutdown, default `False`


## Benchmark with locust 
```bash
locust -f benchmark/locustfile.py
```
And follow the instructions to start benchmarking.