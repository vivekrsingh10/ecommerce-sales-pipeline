# 🛒 E-commerce Sales Pipeline (ETL + Airflow + MySQL + Power BI)

## 📌 Project Overview
This project demonstrates a complete **ETL (Extract → Transform → Load) pipeline** for an e-commerce sales dataset, automated with **Apache Airflow**, stored in **MySQL**, and visualized in **Power BI**.  

It simulates a **real-world Data Engineering workflow** where raw CSV data is ingested, transformed into a star-schema data warehouse, and used to build interactive dashboards.

---

## 🚀 Tech Stack
- **Python (Pandas, MySQL Connector)** → ETL logic  
- **Apache Airflow (Dockerized)** → Workflow orchestration & scheduling  
- **MySQL** → Data warehouse (star schema design)  
- **Docker & Docker Compose** → Containerized Airflow setup  
- **Power BI** → Business intelligence & visualization  

---

## 📂 Project Structure
superstore-etl/
│── airflow-docker/ # Airflow setup (docker-compose)
│ ├── dags/ # Airflow DAGs
│ │ └── superstore_etl.py # Main ETL DAG
│ ├── logs/ # Airflow logs (ignored in git)
│ └── docker-compose.yaml # Docker setup
│
│── data/
│ └── Superstore.csv # Raw source data
│
│── etl/
│ └── etl_script.py # ETL logic (extract, transform, load)
│
│── sql/
│ └── schema.sql # MySQL star schema (dimensions + facts)
│
│── powerbi/
│ └── dashboard.pbix # Power BI dashboard
│
└── README.md # Documentation

## 🛠️ ETL Workflow
1. **Extract**  
   - Reads data from `Superstore.csv`.  

2. **Transform**  
   - Cleans and preprocesses sales data.  
   - Creates a **Star Schema**:  
     - `dim_customer`  
     - `dim_product`  
     - `dim_region`  
     - `dim_date`  
     - `fact_sales`  

3. **Load**  
   - Inserts transformed data into **MySQL warehouse**.  

---

## ⚡ Airflow DAG
- Location: `airflow-docker/dags/superstore_etl.py`  
- Tasks:  
  - `extract_data` → Read CSV  
  - `transform_data` → Apply transformations  
  - `load_superstore_data` → Load into MySQL  
- **Scheduled**: Daily run at midnight  

---

## 🗄️ Database Schema (Star Model)
    dim_customer      dim_product       dim_region       dim_date
         |                 |                 |               |
         |                 |                 |               |
                          fact_sales (sales, quantity, discount, profit)


---

## 📊 Power BI Dashboard
The data warehouse feeds into **Power BI** for analytics.  

### Key Visuals:
- **KPIs (Cards at Top)**  
  - Total Sales  
  - Total Orders  
  - Total Customers  
  - Avg Sales per Order  

- **Sales Trends**  
  - Sales over time (Line chart)  

- **Breakdowns**  
  - Sales by region (Bar chart)  
  - Sales by product category (Pie chart)  
  - Top 10 customers (Table/Bar chart)  

- **Filters (Slicers)**  
  - Region filter  
  - Product category filter  
  - Date filter  

<img width="1525" height="856" alt="Image" src="https://github.com/user-attachments/assets/2af1d3b0-b4de-431a-9a3d-7dbf8bd8673d" />

---






