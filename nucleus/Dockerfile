FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip \
    && mkdir -p /srv/nucleus
WORKDIR /srv/nucleus
COPY requirements.txt ./
RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev \
    && pip install -r requirements.txt \
    && pip install gunicorn \
    && apk del gcc musl-dev
COPY . ./
ENTRYPOINT ["gunicorn", "--chdir", "/srv/nucleus", "--pythonpath", "..", "--bind", "0.0.0.0:5000", "main:app"]
