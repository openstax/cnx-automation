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
    python3-pip \
    python3-dev \
    build-essential \
  && pip3 install --upgrade pip

# Install Tox
RUN pip3 install tox

WORKDIR /code

USER seluser

EXPOSE 5900
EXPOSE 4444
