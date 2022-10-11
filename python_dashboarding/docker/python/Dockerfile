FROM python:3.8

EXPOSE 8050


WORKDIR /app

COPY /requirements.txt /

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt