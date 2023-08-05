FROM        stibbons31/alpine-s6-python3-twisted:py3.6-tx17.9
MAINTAINER  gaetan@xeberon.net

# set environment variables
ENV         PYTHONIOENCODING="UTF-8"
ARG         DEBIAN_FRONTEND="noninteractive"

RUN         apk add --no-cache --update \
                    curl \
                    git \
                    gcc \
                    python3-dev \
                    make \
                    linux-headers \
                    musl-dev

# Injecting files into containers
RUN         mkdir -p /app
WORKDIR     /app

# Keep dependencies on its own Docker FS Layer
# To avoid dependencies reinstall at each code change
COPY        Pipfile* setup-pip.sh /app/
RUN         ./setup-pip.sh
RUN         pipenv install --system

# Building python application in other docker layer

# copy containers's startup files
COPY        root/ /
RUN         mkdir -p /media

# installing main Python module to system
COPY        . /app/
RUN         cd /app \
        &&  pip install .

USER        root
# clean up
RUN         apk del python3-dev \
                make \
                gcc \
                curl \
                linux-headers \
                musl-dev \
        &&  rm  -rf \
                /root/.cache \
                /tmp/*

# Docker configuration
EXPOSE      8086
VOLUME      /config /animes /movies /tv
