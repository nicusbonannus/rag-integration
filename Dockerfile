FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    git curl build-essential libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["python", "app/main.py"]
