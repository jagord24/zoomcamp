# FROM python:3.9

# RUN apt-get install wget
# RUN pip install pandas sqlalchemy psycopg2-binary pyarrow

# WORKDIR /app
# COPY ingest_data.py ingest_data.py

# ENTRYPOINT [ "python", "ingest_data.py" ]


FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2-binary requests

WORKDIR /app
COPY ingest_indego.py ingest_indego.py

ENTRYPOINT [ "python", "ingest_indego.py" ]