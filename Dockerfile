FROM python:3.8

RUN mkdir /youtube_query_monitor
WORKDIR /youtube_query_monitor

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY .env .
COPY manage.py .
COPY youtube_api ./youtube_api
COPY youtube_query_monitor ./youtube_query_monitor
