from dynaconf import Dynaconf
from loguru import logger
from transformers.pipelines import PIPELINE_REGISTRY

settings = Dynaconf(
    settings_files=["hf_serve/settings.py", "hf_serve/.secrets.toml"],
    environments=True,
    envvar_prefix="HF_SERVE",
)
print(settings.MODEL)
PIPELINE_REGISTRY.check_task(task=settings.TASK)

logger.info(f"Loaded settings: {dict(settings)}")
