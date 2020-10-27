FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /srv/nucleus

COPY . ./

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get -y install gcc \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install uwsgi

ENTRYPOINT ["uwsgi", \
            "--strict", \
            "--disable-logging", \
            "--log-5xx", \
            "--max-requests", "1000", \
            "--max-worker-lifetime", "3600", \
            "--reload-on-rss", "2048", \
            "--worker-reload-mercy", "60", \
            "--http-socket", "0.0.0.0:5000", \
            "--chdir", "/srv/nucleus/", \
            "--pythonpath", "/srv/", \
            "--wsgi-file", "main.py", \
            "--callable", "app", \
            "--processes", "4", \
            "--master", \
            "--vacuum", \
            "--need-app"]
