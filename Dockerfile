FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip install spacy
RUN python -m spacy download en_vectors_web_lg

RUN pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system

COPY . /usr/src/app
