from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector

# ✅ Absolute CSV path inside the container
CSV_PATH = "/opt/airflow/data/Superstore.csv"

# ETL Function
def load_data_to_mysql():
    # Read CSV
    df = pd.read_csv(CSV_PATH, encoding="ISO-8859-1")

    # Connect to MySQL (update host/user/pass as per your MySQL setup)
    conn = mysql.connector.connect(
        host="host.docker.internal",   # allows container to connect to host MySQL
        user="root",
        password="Singh@2357",
        database="superstore_dw"
    )
    cursor = conn.cursor()

    # Insert data into fact_sales (simplified for demo)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO fact_sales (order_id, order_date, ship_date, ship_mode, customer_id, product_id, region_id, sales, quantity, discount, profit)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row['Order ID'], row['Order Date'], row['Ship Date'], row['Ship Mode'],
            row['Customer ID'], row['Product ID'], row['Region'], 
            row['Sales'], row['Quantity'], row['Discount'], row['Profit']
        ))
    conn.commit()
    cursor.close()
    conn.close()

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    dag_id='superstore_etl',
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    etl_task = PythonOperator(
        task_id='load_superstore_data',
        python_callable=load_data_to_mysql,
    )

    etl_task

