FROM python:3.7-buster

RUN pip install flask
RUN pip install peewee
RUN pip install schema
RUN pip install requests
RUN pip install psycopg2
EXPOSE 5000
COPY /api8inf349 /api8inf349
#COPY /api8inf349/__init__.py /api8inf349/__init__.py
#COPY /api8inf349/models.py /api8inf349/models.py
#COPY /api8inf349/product_table_init.py /api8inf349/product_table_init.py
#COPY /api8inf349/schemas.py /api8inf349/schemas.py
#COPY /api8inf349/schemas_validation.py /api8inf349/schemas_validation.py
#COPY /api8inf349/services.py /api8inf349/services.py
#COPY /api8inf349/url.py /api8inf349/url.py
#COPY /docker-compose.yml /
#COPY /Dockerfile /
#COPY /README.md /




CMD FLASK_DEBUG=1 FLASK_APP=api8inf349 FLASK_ENV=development flask run --host=0.0.0.0