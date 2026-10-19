FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py ./server.py
COPY index.html ./index.html
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "-u", "server.py"]
