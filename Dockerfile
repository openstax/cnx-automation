FROM openstax/selenium-chrome-debug:latest

USER root

# Install wait-for and dependencies
RUN set -x \
  && apt-get update \
  && apt-get install curl netcat --no-install-recommends -qqy \
  && rm -rf /var/lib/apt/lists/* \
  && curl https://raw.githubusercontent.com/eficode/wait-for/828386460d138e418c31a1ebf87d9a40f5cedc32/wait-for -o /usr/local/bin/wait-for \
  && chmod a+x /usr/local/bin/wait-for

COPY --chown=seluser:seluser . /code

WORKDIR /code

RUN pip3 install -r requirements.txt

USER seluser
