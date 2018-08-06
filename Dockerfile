# Inspired by: https://hub.docker.com/r/b4handjr/selenium-firefox/~/dockerfile/
FROM openstax/selenium-chrome:latest

USER root

COPY . /code

WORKDIR /code

# Install Tox
RUN pip3 install tox

USER seluser
