FROM openstax/selenium-chrome-debug:latest

USER root

COPY . /code

WORKDIR /code

# Install Tox
RUN pip3 install tox

USER seluser
