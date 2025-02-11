## Importing required libraries

from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import logging

## Defining file URLs

customer_url="https://raw.githubusercontent.com/elreddy/E-commerce_Data_Pipeline/refs/heads/main/customers.csv"
orders_url="https://raw.githubusercontent.com/elreddy/E-commerce_Data_Pipeline/refs/heads/main/orders.csv"

## Defining dag arguments

default_arguments= {
    "owner": "lokesh",
    "start_date": datetime(2025,2,9)
}

## Defining the DAG

dag= DAG(
    "ecommerce_pipeline",
    default_args=default_arguments,
    description = "ETL pipeline for E-commerce data",
    schedule_interval= timedelta(days=1),
    catchup=False,
)

## Defining the tasks

## Task 1: Extract the customer file form source and provide the required previlages and drop it in the SourceInputDirectory.

Extract_Customer_File= BashOperator(
    task_id="extract_customer_file",
    bash_command= f"""
                    wget -O /home/lokesh/SourceInputDir/E_Commerce_Data/customers.csv {customer_url}
                    chmod 644 /home/lokesh/SourceInputDir/E_Commerce_Data/customers.csv
                    """,
    dag= dag
)

## Task 2: Extract the orders file form source and provide the required previlages and drop it in the SourceInputDirectory.

Extract_Orders_File= BashOperator(
    task_id="extract_orders_file",
    bash_command= f"""
                      wget -O /home/lokesh/SourceInputDir/E_Commerce_Data/orders.csv {orders_url}
                      chmod 644 /home/lokesh/SourceInputDir/E_Commerce_Data/orders.csv
                      """,
    dag= dag
)

## Task 3: Loading the Customer data into MySQL Database.

mysql_command= """
mysql --defaults-extra-file=~/.my.cnf <<EOF
use airflow_pipeline; 
CREATE TABLE IF NOT EXISTS customers(customer_id INT PRIMARY KEY, customer_name varchar(50), email varchar(50), city varchar(30));
LOAD DATA LOCAL INFILE '/home/lokesh/SourceInputDir/E_Commerce_Data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;
EOF
"""

Loading_Customer_Data= BashOperator(
    task_id= "Loading_customer_data",
    bash_command= mysql_command,
    dag= dag
)

## Task 4: Loading the Orders data into PostgreSQL Database.

psql_command= """
psql -U airflow_user -d airflow_pipeline -v ON_ERROR_STOP=1 -c "
CREATE TABLE IF NOT EXISTS orders(order_id INT PRIMARY KEY , customer_id INT, order_date DATE, customer_amount FLOAT);"
psql -U airflow_user -d airflow_pipeline -c "\COPY orders FROM '/home/lokesh/SourceInputDir/E_Commerce_Data/orders.csv' with (FORMAT csv, HEADER true);"
"""

Loading_Orders_Data= BashOperator(
    task_id= "Loading_orders_data",
    bash_command= psql_command,
    dag= dag
)


## Task 5: Moving the processed files to another directory.

Moving_files_ProcessedDirectory= BashOperator(
    task_id= "Moving_files_otherDirectory",
    bash_command= """
                     mv /home/lokesh/SourceInputDir/E_Commerce_Data/customers.csv /home/lokesh/SourceInputDir/E_Commerce_Data/Processed_files
                     mv /home/lokesh/SourceInputDir/E_Commerce_Data/orders.csv /home/lokesh/SourceInputDir/E_Commerce_Data/Processed_files
                     """,
    dag= dag
)


## Task 6: Joinning the two tables to get the required Customers_Orders data using FDW.

fdw_sql_command= """
CREATE EXTENSION IF NOT EXISTS mysql_fdw;
CREATE SERVER IF NOT EXISTS mysql_server FOREIGN DATA WRAPPER mysql_fdw
OPTIONS (host 'localhost', port '3306');
CREATE USER MAPPING IF NOT EXISTS FOR airflow_user SERVER mysql_server
OPTIONS (username '{{conn.mysql_conn.login}}', password '{{conn.mysql_conn.password}}');

DROP FOREIGN TABLE IF EXISTS customers_fdw;

CREATE FOREIGN TABLE IF NOT EXISTS customers_fdw(
    customer_id INT,
    customer_name varchar(50),
    email varchar(50),
    city varchar(30)
)SERVER mysql_server
OPTIONS(dbname 'airflow_pipeline', table_name 'customers');

DROP TABLE IF EXISTS customers_orders;

CREATE TABLE IF NOT EXISTS customers_orders as 
SELECT c.customer_id, c.customer_name, c.email, c.city, o.order_id, o.order_date, o.customer_amount
FROM customers_fdw as c
INNER JOIN orders as o
ON c.customer_id=o.customer_id;
"""

Creating_Customers_Orders_table= SQLExecuteQueryOperator(
    task_id="Creating_Customers_Orders_table",
    conn_id="postgresql_conn",
    sql= fdw_sql_command,
    dag= dag
)

## Task 7: Extracting the requiered Customers_Orders data and saving it in a csv file in OutputDirectory.

# Defining Python script to extract and load data in csv.

def extract_customers_orders_data():
    logging.info("Starting data extraction from PostgreSQL...")
    try:
        postgres_hook= PostgresHook(postgres_conn_id= "postgresql_conn")
        conn = postgres_hook.get_conn()
        logging.info("Connection got established successfully...")

        query= "SELECT * FROM customers_orders;"
        customers_orders_df = pd.read_sql(query, conn)
        logging.info(f"Retrieved {len(customers_orders_df)} records from customers_orders table.")

        customers_orders_df.to_csv(f"/home/lokesh/OutputDir/E_Commerce_Data/customers_orders_{date.today()}.csv", index=False)
        logging.info("Data extracted successfully and saved in csv file.")
        
    except Exception as e:
        logging.error(f"Error during data extraction: {e}")
        raise  

    finally:
        # Close the connection
        conn.close()
        logging.info("PostgreSQL connection closed.")

Extracting_Customers_Orders_Data= PythonOperator(
    task_id= "Extracting_Customers_Orders_Data",
    python_callable= extract_customers_orders_data,
    dag= dag
)

## Defining the pipeline

Extract_Customer_File >> Extract_Orders_File >> [Loading_Customer_Data,Loading_Orders_Data] >> Moving_files_ProcessedDirectory
[Loading_Customer_Data,Loading_Orders_Data] >> Creating_Customers_Orders_table >> Extracting_Customers_Orders_Data
