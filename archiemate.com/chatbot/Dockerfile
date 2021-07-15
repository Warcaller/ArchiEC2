FROM python:3.9-slim

RUN groupadd -g 1000 ubuntu && useradd --create-home --home-dir /chatbot --shell /bin/bash -g ubuntu -u 1000 ubuntu

USER ubuntu
WORKDIR /chatbot

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY ./archiemate.com/chatbot/Pipfile ./archiemate.com/chatbot/Pipfile.lock ./archiemate.com/chatbot/ArchieMateBot.py /chatbot/
ADD ./archiemate.com/chatbot/ArchieMate /chatbot/ArchieMate
RUN rm -r /chatbot/__pycache__ /chatbot/Archiemate/__pycache__ /chatbot/ArchieMate/Twitch/__pycache__ /chatbot/logs/ArchieMate.log* || true
RUN mkdir -p /chatbot/logs && touch /chatbot/logs/ArchieMate.log /chatbot/logs/IRC.log

USER root

RUN pip install --upgrade pip && \
    pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pipenv install --deploy --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y

USER ubuntu
