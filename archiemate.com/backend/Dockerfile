FROM python:3.8.0-slim

WORKDIR /app

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./archimond7450.com/backend/Pipfile ./archimond7450.com/backend/Pipfile.lock ./archimond7450.com/backend/manage.py ./archimond7450.com/backend/wsgi-entrypoint.sh /app/
RUN pip install --upgrade pip && \
    pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pipenv install --deploy --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y

ADD ./archimond7450.com/backend/apps /app/apps
ADD ./archimond7450.com/backend/server /app/server

RUN chmod +x /app/wsgi-entrypoint.sh
