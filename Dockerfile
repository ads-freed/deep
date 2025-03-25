FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/uploads /app/logs
RUN chmod -R 777 /app/uploads /app/logs

EXPOSE 5000

CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:create_app()", "--bind", "0.0.0.0:5000"]
