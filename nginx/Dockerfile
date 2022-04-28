FROM alpine:latest

RUN apk --update add nginx && \
    rm -rf /etc/nginx/sites-enabled/ && \
    mkdir -p /run/nginx && \
    rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /etc/nginx/http.d/*.conf && \
    rm -rf /var/cache/apk/*

COPY http.d/app.conf /etc/nginx/http.d/app.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]

