# Inspired by: https://hub.docker.com/r/b4handjr/selenium-firefox/~/dockerfile/
FROM selenium/standalone-chrome-debug

USER root

# Install curl
RUN apt-get update -qqy \
  && apt-get -qqy install \
    curl

# Install python
RUN apt-get update -qqy \
  && apt-get -qqy install \
    python-pip \
    python-dev \
    build-essential \
  && pip install --upgrade pip

# Install Tox
RUN pip install tox

WORKDIR /code

USER seluser

EXPOSE 5900
EXPOSE 4444
