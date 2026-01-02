FROM python:3.12-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install playwright && playwright install --with-deps
COPY . .
ENV PYTHONUNBUFFERED=1
