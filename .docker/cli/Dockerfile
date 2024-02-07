FROM python:3.9.18-bullseye as cli

VOLUME app
WORKDIR app

COPY src/requirements.txt app/requirements.txt
# The `--break-system-packages` flag is used beacuse the Alpine distro can install Python packages.
# Install packages from the `requirements.txt` can break previously installed packages
RUN pip3 install --no-cache-dir --break-system-packages -r app/requirements.txt
