FROM python:3-slim-stretch

RUN pip --no-cache-dir install matplotlib

RUN mkdir -p /opt/waqi-station-report
WORKDIR /opt/waqi-station-report

COPY waqi-sr.py .
