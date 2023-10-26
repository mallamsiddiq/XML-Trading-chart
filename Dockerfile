

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN mkdir /ft9ja


WORKDIR /ft9ja


ADD . /ft9ja/

# COPY spinup.sh /app/spinup.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn ft9ja.wsgi:application --bind 0.0.0.0:$PORT