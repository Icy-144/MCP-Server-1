FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt

COPY . .

CMD ["python", "server.py"]