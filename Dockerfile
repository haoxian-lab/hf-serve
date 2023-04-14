# Use the official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .
COPY hf_serve ./hf_serve
# Install the necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgomp1 \
        && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry && poetry config virtualenvs.create false && poetry install && rm -rf ~/.cache

# Install pytorch with cuda
RUN pip3 install torch  --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir



# Expose the port that the application will run on
EXPOSE 80

# Start the application when the container starts
CMD ["python", "-m", "uvicorn", "hf_serve.serving_fastapi:app", "--host", "0.0.0.0", "--port", "80"]

