FROM python:3.8

RUN mkdir /youtube_query_monitor
WORKDIR /youtube_query_monitor

RUN export C_INCLUDE_PATH=/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/Headers

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY .env .
COPY manage.py .
COPY youtube_api .
COPY youtube_query_monitor .
