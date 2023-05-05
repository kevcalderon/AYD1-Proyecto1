FROM jenkins/agent:alpine

USER root

# Instalación de Node.js y npm
RUN apk add --no-cache nodejs npm

COPY requirements.txt /home/jenkins/agent/requirements.txt

# Instalación de Python3 y pip
RUN apk add --no-cache python3 py3-pip && \
    ln -sf python3 /usr/bin/python && \
    ln -sf pip3 /usr/bin/pip 

RUN pip install -r /home/jenkins/agent/requirements.txt


# Instalación de Docker
RUN apk add --no-cache docker

USER jenkins
