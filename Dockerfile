FROM python:3.10.5-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . .

RUN pip install -r requirements.txt && \
playwright install chromium && playwright install-deps && \
apt-get update -y
