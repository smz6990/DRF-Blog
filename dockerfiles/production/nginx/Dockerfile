FROM nginx:1.21.6-alpine

COPY ./config/* /etc/nginx/
COPY ./entrypoint.sh /entrypoint.sh

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /entrypoint.sh


CMD ["/entrypoint.sh"]