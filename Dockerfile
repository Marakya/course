FROM python:3.14

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync

COPY . .

EXPOSE 8000

# main.py - яндекс
# CMD ["uv", "run", "python", "main.py"]

# app.py - langflow
# CMD ["uv", "run", "python", "app.py"]