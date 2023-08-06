FROM python:3.9-slim

LABEL maintainer="bensong2017@gmail.com"

COPY ./deploy/http_server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -i https://pypi.douban.com/simple/ -r /tmp/requirements.txt

COPY ./deploy/http_server/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./deploy/http_server/gunicorn_conf.py /app/gunicorn_conf.py

COPY ./ /app
WORKDIR /

ENV PYTHONPATH=/app

EXPOSE 9000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]