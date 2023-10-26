


# CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT

FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /ft9ja
WORKDIR /ft9ja

# Copy your application code
ADD . /ft9ja/

# Copy the entrypoint script
COPY entry.sh /ft9ja/entry.sh

# Make the entrypoint script executable
RUN chmod +x /ft9ja/entry.sh

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the entrypoint to run your custom entrypoint script
ENTRYPOINT ["/ft9ja/entrypoint.sh"]
