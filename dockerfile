# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /PRELLO

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

ENV FLASK_APP=main/index.py
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# command to run on container start
# CMD [ "flask", "run" ]