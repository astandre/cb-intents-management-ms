FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

#WORKDIR /app/kbsbot/intents_managment
EXPOSE 8002
#CMD ["gunicorn", "-b", "0.0.0.0:8002", "run:app"]
#CMD gunicorn -c /app/gunicorn.ini
CMD ["intents_managment", "-d", "--config-file", "/app/settings.ini"]
