FROM python:3-slim-stretch

RUN addgroup --system app \
 && adduser --system --ingroup app app

RUN pip --no-cache-dir install matplotlib

WORKDIR /home/app

COPY waqi-sr.py .

RUN chown -R app:app ./
USER app
