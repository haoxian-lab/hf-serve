import sys

import torch

if sys.platform == "darwin":
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda:0"
else:
    DEVICE = "cpu"

MODEL = "cardiffnlp/tweet-topic-21-multi"
