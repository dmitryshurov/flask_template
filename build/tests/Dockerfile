FROM ubuntu:20.04

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip

WORKDIR /src
COPY build/tests/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./tests ./tests

ENTRYPOINT pytest tests 
