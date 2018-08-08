FROM openstax/selenium-chrome:latest

COPY . /code

ENV HEADLESS=True
WORKDIR /code

# Install Tox
RUN pip3 install tox
