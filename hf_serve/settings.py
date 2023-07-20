import sys

import torch

USE_GPU = False
DEVICE = "cpu"
if USE_GPU:
    if sys.platform == "darwin":
        DEVICE = "mps"
    elif torch.cuda.is_available():
        DEVICE = "cuda:0"

MODEL = "cardiffnlp/tweet-topic-21-multi"
TASK = "text-classification"
MODEL_CACHE_DIR = "/tmp/hf_serve"
CLEAR_MODEL_CACHE_ON_SHUTDOWN = False
