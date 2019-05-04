FROM python:3.7-slim

ADD requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD *.py /app/

CMD python /app/updater.py
