
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir "psycopg[binary]"

ENV PYTHONUNBUFFERED=1

CMD ["python", "server.py"]
