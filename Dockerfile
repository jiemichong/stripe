FROM python:3.9-slim
WORKDIR /usr/src/server
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src .
CMD ["python", "./server.py"]