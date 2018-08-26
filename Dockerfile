FROM openstax/selenium-chrome:latest

USER root

ARG USER=cnx
ARG USER_ID=1001
ARG GROUP_ID=1001

RUN groupadd -g ${GROUP_ID} ${USER} && \
    useradd -u ${USER_ID} -s /bin/sh -g ${USER} ${USER}

COPY . /code

WORKDIR /code

# Install Tox
RUN pip3 install tox
