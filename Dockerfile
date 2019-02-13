FROM python:3.6-alpine
COPY setup.py README.rst production.ini CHANGES.txt /app/
COPY memory /app/memory
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libxml2-dev \
    libxslt-dev \
    pcre-dev \
    zlib-dev &&\
    mkdir filestorage
RUN pip install -e .  && pip install -e ".[testing]"
EXPOSE 6543
VOLUME /app/filestorage
CMD pserve production.ini
