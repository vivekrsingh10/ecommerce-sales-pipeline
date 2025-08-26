import pandas as pd
import mysql.connector
from datetime import datetime

# 1. Connect to MySQL
conn = mysql.connector.connect(
    host="host.docker.internal",
    user="root",
    password="Singh@2357",
    database="superstore_dw"
)
cursor = conn.cursor()


# 2. Load CSV
df = pd.read_csv("/opt/airflow/data/Superstore.csv", encoding="ISO-8859-1")

# Convert date columns to MySQL-compatible format (YYYY-MM-DD)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m/%d/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%m/%d/%Y')


# 3. Insert Customers
customers = df[['Customer ID','Customer Name','Segment']].drop_duplicates()
for _, row in customers.iterrows():
    cursor.execute("""
        INSERT INTO dim_customer (customer_id, customer_name, segment)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE customer_name=VALUES(customer_name);
    """, (row['Customer ID'], row['Customer Name'], row['Segment']))

# 4. Insert Products
products = df[['Product ID','Category','Sub-Category','Product Name']].drop_duplicates()
for _, row in products.iterrows():
    cursor.execute("""
        INSERT INTO dim_product (product_id, category, sub_category, product_name)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE product_name=VALUES(product_name);
    """, (row['Product ID'], row['Category'], row['Sub-Category'], row['Product Name']))

# 5. Insert Regions
regions = df[['Country','Region','State','City','Postal Code']].drop_duplicates()
for _, row in regions.iterrows():
    cursor.execute("""
        INSERT INTO dim_region (country, region, state, city, postal_code)
        VALUES (%s, %s, %s, %s, %s);
    """, (row['Country'], row['Region'], row['State'], row['City'], str(row['Postal Code'])))

# 6. Insert Dates
dates = pd.to_datetime(df['Order Date']).drop_duplicates()
for d in dates:
    cursor.execute("""
        INSERT INTO dim_date (date_id, year, quarter, month, day, weekday)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE year=VALUES(year);
    """, (d.date(), d.year, (d.month-1)//3 + 1, d.month, d.day, d.strftime('%A')))

# 7. Insert Fact Sales
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO fact_sales 
        (order_id, order_date, ship_date, customer_id, product_id, region_id, sales, quantity, discount, profit)
        VALUES (%s,%s,%s,%s,%s,
            (SELECT region_id FROM dim_region WHERE city=%s LIMIT 1),
            %s,%s,%s,%s);
    """, (
        row['Order ID'], row['Order Date'], row['Ship Date'],
        row['Customer ID'], row['Product ID'], row['City'],
        row['Sales'], row['Quantity'], row['Discount'], row['Profit']
    ))

# Commit + Close
conn.commit()
cursor.close()
conn.close()

print("✅ Data loaded successfully into warehouse!")
