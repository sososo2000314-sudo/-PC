FROM python:3.13-slim
WORKDIR /app
COPY index.html ./index.html
COPY server.py ./server.py
COPY requirements.txt ./requirements.txt
EXPOSE 8000
CMD ["python", "-u", "server.py"]
