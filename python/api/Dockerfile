FROM python:3

ADD *.py /

COPY tank_database.db /app

RUN pip install serial numpy telegram plot requests pytz passlib python-dateutil

CMD [ "python", "./monitor.py" ]
