# specific for Raspberry Pi Zero W 
# FROM arm32v6/python:2.7.17-alpine3.11

# generic version
FROM python:2.7.17-buster

RUN python -m pip install pyserial

COPY MessageBridge /opt/srf-stick-receiver
COPY config /config
COPY logs /logs

CMD ["/opt/srd-stick-receiver/MessageBridge.py"]
