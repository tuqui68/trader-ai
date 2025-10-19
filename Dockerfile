FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    git \
    ca-certificates \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 2) Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) Copy your source code
COPY . .

# 4) Expose and run
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
