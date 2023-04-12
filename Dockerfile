# Use the official Python image as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgomp1 \
        && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Install pytorch with cuda
RUN pip install torch==1.9.1+cu111 -f https://download.pytorch.org/whl/cu111/torch_stable.html

# Copy the application code into the container
COPY app.py .

# Expose the port that the application will run on
EXPOSE 80

# Start the application when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

