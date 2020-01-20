FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/settings.ini
COPY docker/kg.rdf /app/kg.rdf

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

ENV KG_URL="/app/kg.rdf"
ENV BASE_URL="http://127.0.0.1"

WORKDIR /app/kbsbot/intents_managment

EXPOSE 8002
CMD ["gunicorn", "-b", "0.0.0.0:8002", "run:app"]

