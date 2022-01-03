FROM nginx:1.21

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y gettext-base

COPY ./build/configs/nginx/conf.d /etc/nginx/conf.d
COPY ./build/scripts/envsubst.sh /
WORKDIR /etc/nginx/conf.d

CMD /envsubst.sh backend.conf pgadmin.conf && nginx -g "daemon off;"