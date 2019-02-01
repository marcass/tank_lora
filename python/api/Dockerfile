FROM python:3

ADD *.py /

COPY tank_database.db /

RUN pip install pyserial numpy telegram plot requests pytz passlib python-dateutil telepot

CMD [ "python", "./monitor.py" ]
