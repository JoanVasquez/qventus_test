FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y python3-distutils

WORKDIR /app

EXPOSE 8000

# Optional flag for dev dependencies
ARG DEV=false

COPY requirements.txt .
COPY requirements.dev.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt && \
    if [ "$DEV" = "true" ]; then pip install -r requirements.dev.txt; fi

COPY . .
