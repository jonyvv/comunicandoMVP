FROM nginx:alpine

# limpiar nginx default
RUN rm -rf /usr/share/nginx/html/*

# copiar html
COPY htmlycss/ /usr/share/nginx/html/
RUN mkdir -p /usr/share/nginx/html/htmlycss
COPY htmlycss/ /usr/share/nginx/html/htmlycss/
# copiar js
COPY js/ /usr/share/nginx/html/js/

EXPOSE 80