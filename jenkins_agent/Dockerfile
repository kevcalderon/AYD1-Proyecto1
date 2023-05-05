FROM jenkins/agent:alpine

USER root

# Instalación de Node.js y npm
RUN apk add --no-cache nodejs npm

# Instalación de Python3 y pip
RUN apk add --no-cache python3 py3-pip && \
    ln -sf python3 /usr/bin/python && \
    ln -sf pip3 /usr/bin/pip

# Instalación de Docker
RUN apk add --no-cache docker

USER jenkins
