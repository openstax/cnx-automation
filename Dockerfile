# Inspired by: https://hub.docker.com/r/b4handjr/selenium-firefox/~/dockerfile/
FROM selenium/standalone-chrome-debug

USER root

# Install higher level packages
RUN apt-get update -qqy \
  && apt-get -qqy install \
    curl \
    software-properties-common \
    python-software-properties \
  && add-apt-repository ppa:jonathonf/python-3.6

# Install python3.6
RUN apt-get update -qqy \
  && apt-get -qqy install \
    python3.6 \
    python3-pip \
    python3.6-dev \
    build-essential \
  && pip3 install --upgrade pip

# Install Tox
RUN pip3 install tox

WORKDIR /code

USER seluser

EXPOSE 5900
EXPOSE 4444
