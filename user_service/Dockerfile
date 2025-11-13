# user_service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "main:app"]