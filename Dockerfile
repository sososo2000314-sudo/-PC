FROM python:3.13-slim
WORKDIR /app
COPY index.html ./index.html
COPY server.py ./server.py

EXPOSE 8000
CMD ["python", "-u", "server.py"]
