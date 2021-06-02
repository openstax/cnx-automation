# See https://github.com/openstax/docker-qa for more information about this base image.
FROM openstax/selenium-chrome-debug:20210602.073227

USER root

# Install wait-for and dependencies
RUN set -x \
  && apt-get update \
  && apt-get install curl netcat --no-install-recommends -qqy \
  && rm -rf /var/lib/apt/lists/*

# Install rustup
RUN curl --proto '=https' -y --tlsv1.2 -sSf https://sh.rustup.rs | sh
RUN pip install -U pip

COPY --chown=seluser:seluser . /code

WORKDIR /code

RUN pip3 install -r requirements.txt

USER seluser