# Docker image for squash-dash microservice
FROM python:3.6-slim
LABEL maintainer "afausti@lsst.org"
WORKDIR /opt
COPY . .

# gcc is required to compile uwsgi
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc

RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /opt/squash

RUN groupadd -r uwsgi_grp && useradd -r -g uwsgi_grp uwsgi
RUN chown -R uwsgi:uwsgi_grp /opt/squash
USER uwsgi

EXPOSE 8000
CMD ["uwsgi", "uwsgi.ini"]



