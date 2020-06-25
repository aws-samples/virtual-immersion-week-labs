FROM alpine:latest

MAINTAINER Pablo Pölcher <polcher@amazon.com>

RUN apk --update add nginx
RUN mkdir -p /run/nginx
RUN touch /run/nginx/nginx.pid

COPY 2048 /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
