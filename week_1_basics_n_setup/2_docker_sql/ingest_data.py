import os
import argparse
from time import time
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if url.endswith('.parquet'):


        output_name = 'output.parquet'

        os.system(f"wget {url} -O {output_name}")
        parquet_file = pq.ParquetFile(output_name)
        parquet_size = parquet_file.metadata.num_rows

        df = pq.read_table(output_name).to_pandas()
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        # default (and max) batch size
        index = 65536
        for i in parquet_file.iter_batches(use_threads=True):
            t_start = time()
            print(f'Ingesting {index} out of {parquet_size} rows ({index / parquet_size:.0%})')
            i.to_pandas().to_sql(name=table_name, con=engine, if_exists='append')
            index += 65536
            t_end = time()
            print(f'\t- it took %.1f seconds' % (t_end - t_start))

        # df.to_sql(name=table_name, con=engine, if_exists='append')
    
    else:
        if url.endswith('.csv.gz'):
            csv_name = 'output.csv.gz'
        else:
            csv_name = 'output.csv'

        os.system(f"wget {url} -O {csv_name}")


        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df.to_sql(name=table_name, con=engine, if_exists='append')
    
        while True: 

            try:
                t_start = time()
                
                df = next(df_iter)

                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

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

    args = parser.parse_args()

    main(args)