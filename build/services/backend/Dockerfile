FROM ubuntu:20.04

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip uwsgi-plugin-python3 gettext-base

WORKDIR /src
COPY ./build/services/backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./source ./source
COPY ./build/configs/uwsgi/backend.ini backend.ini
COPY ./build/scripts/envsubst.sh .

ENTRYPOINT ./envsubst.sh backend.ini && uwsgi --ini backend.ini
