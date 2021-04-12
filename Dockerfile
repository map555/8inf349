FROM python:3.7-buster

COPY requirements.txt /
RUN pip install -r requirements.txt

EXPOSE 5000
COPY /api8inf349 /api8inf349
CMD FLASK_DEBUG=1 FLASK_APP=api8inf349 FLASK_ENV=development flask run --host=0.0.0.0