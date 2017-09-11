FROM arm32v6/alpine

MAINTAINER SimonStJG <Simon.StJG@gmail.com>

RUN apk add --update python3 py3-pip && rm -rf /var/cache/apk/*

COPY ./requirements /requirements
RUN python3 -m pip install -r requirements/docker.txt
COPY ./dailywhiskers /dailywhiskers
COPY config.json /config.json

# For prometheus
EXPOSE 8000

CMD python3 dailywhiskers/runner.py
