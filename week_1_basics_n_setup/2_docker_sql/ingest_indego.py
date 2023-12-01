import os
import argparse
from time import time
# import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
import requests
import zipfile

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = params.file_name

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    subfolder = 'indego_data'
    os.makedirs(subfolder, exist_ok=True)

    url = 'https://bicycletransit.wpenginepowered.com/wp-content/uploads/2023/10/indego-trips-2023-q3.zip'
    response = requests.get(url)
    with open(os.path.join(subfolder, 'indego-trips-2023-q3.zip'), 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile(os.path.join(subfolder, 'indego-trips-2023-q3.zip'), 'r') as zip_ref:
        zip_ref.extractall(subfolder)

    df_iter = pd.read_csv(os.path.join(subfolder, file_name), iterator=True, chunksize=100000)
    df = next(df_iter)
    df['end_lat'] = pd.to_numeric(df['end_lat'], errors='coerce')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df['end_lat'] = pd.to_numeric(df['end_lat'], errors='coerce')


            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest data to Postgres")

    # user
    # password
    # host
    # port
    # database name
    # table name,
    # url of data

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database for postgres")
    parser.add_argument("--table_name", help="name of destination table")
    parser.add_argument("--url", help="url of data to ingest")
    parser.add_argument("--file_name", help="name of file to ingest from within the .zip")

    args = parser.parse_args()

    main(args)