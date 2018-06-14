FROM python:3.6-slim

ENV INSTALL_PATH /farmers_market_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

RUN flask init-db

CMD  gunicorn -b 0.0.0.0:8000 -w 2 --access-logfile - "app:create_app()"