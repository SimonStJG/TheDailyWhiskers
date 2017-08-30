FROM arm32v7/python:3.6

MAINTAINER SimonStJG <Simon.StJG@gmail.com>

COPY ./requirements /requirements
RUN pip install -r requirements/docker.txt
COPY ./dailywhiskers /dailywhiskers
COPY config.json /config.json

# For prometheus
EXPOSE 8000

CMD python3 dailywhiskers/runner.py
