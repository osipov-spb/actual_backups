FROM ubuntu:latest
MAINTAINER Dmitry Osipov 'tellan.dm@gmail.com'
RUN apt-get update -qy
RUN apt-get install -qy python3.10 python3-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3","app.py"]