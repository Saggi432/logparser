FROM ubuntu:16.04
RUN apt-get update && \
    apt-get -y install python3-pip

RUN pip3 install apache-log-parser && \
    pip3 install Flask

COPY app.py /opt/

CMD python3 /opt/app.py
