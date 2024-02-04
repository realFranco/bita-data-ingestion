FROM alpine:3.19 as cli

VOLUME app
WORKDIR app

RUN apk update --no-cache && \
    apk add \
        bash=5.2.21-r0 \
        postgresql-client \
        python3=3.11.6-r1 \
        python3-dev \
        py3-pip \
        gcc \
        musl-dev \
        postgresql-libs \
        postgresql-dev

COPY src/requirements.txt app/requirements.txt
# The `--break-system-packages` flag is used beacuse the Alpine distro can install Python packages.
# Install packages from the `requirements.txt` can break previously installed packages
RUN pip3 install --no-cache-dir --break-system-packages -r app/requirements.txt
