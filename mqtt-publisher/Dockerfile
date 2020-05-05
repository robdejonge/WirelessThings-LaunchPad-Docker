# specific for Raspberry Pi Zero W
# FROM arm32v6/python:2.7.17-alpine3.11

# generic version
FROM python:2.7.17-buster

RUN pip install paho-mqtt
COPY mqtt-publisher.py /usr/local/bin/mqtt-publisher.py

EXPOSE 50140/udp

CMD ["/usr/local/bin/mqtt-publisher.py"]
