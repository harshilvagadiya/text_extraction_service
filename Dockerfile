FROM --platform=linux/amd64 python:3.13

WORKDIR /usr/backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt /usr/backend/

RUN sed -i '/pywin32/d' /usr/backend/requirements.txt

RUN pip install --no-cache-dir -r /usr/backend/requirements.txt

COPY . /usr/backend/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.main:backend_app --host 0.0.0.0 --port 8000"]
