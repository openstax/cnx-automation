FROM openstax/selenium-chrome:latest

USER root

COPY . /code

WORKDIR /code

# Install Tox
RUN pip3 install tox

