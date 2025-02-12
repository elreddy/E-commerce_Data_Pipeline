# E-Commerce Data Pipeline with Apache Airflow

## Project Overview

This project demonstrates a **data pipeline for an E-Commerce dataset** using **Apache Airflow**, **MySQL**, and **PostgreSQL**. The pipeline performs **ETL (Extract, Transform, Load)** operations to efficiently ingest, process, and export customer and order data. It also showcases the seamless integration of file-based data with an RDBMS using ETL tools, enabling cross-database connections for data transformation and processing.  

## Architecture
![Architecture Diagram](Architecture.JPG)

## Dataset Description

This repository contains two datasets used for building a data pipeline: [Repository](Dataset)
1. **customers.csv** – Contains customer-related information such as customer ID, name, contact details, and location.  
2. **orders.csv** – Includes order details such as order ID, customer ID, order date, total amount, and status.
 
## Entity Relationship Diagram for the Dataset(ERD) 
![ERD](ERD.PNG)

## Technologies Used

- **GitHub** (CSV file storage)
- **Apache Airflow** (Workflow Orchestration)
- **PostgreSQL** (Orders Data & Transformation)
- **MySQL** (Customers Data Storage)
- **Foreign Data Wrapper (FDW)** (Cross-database queries)
- **Python & Pandas** (Data Processing)
- **Ubuntu** (Operating System)
- **pgAdmin 4** (ERD Generation)
- **Lucidchart** (Architecture Diagram)
  
## Data Flow Architecture

1. **Extract Data**: Download CSV files from a remote GitHub repository using `wget`.
2. **Load Data**:
   - Load `customers.csv` into **MySQL** using `LOAD DATA INFILE`.
   - Load `orders.csv` into **PostgreSQL** using `COPY`.
3. **Transform Data**:
   - Use **PostgreSQL FDW** (Foreign Data Wrapper) to join MySQL and PostgreSQL data.
   - Store the transformed results in **PostgreSQL**.
4. **Export Processed Data**: Save the final output as a CSV file.
5. **Logging & Monitoring**:
   - Detailed logs for tracking execution steps.
   - Airflow UI for DAG execution monitoring.

## Prerequisites :

Before setting up the data pipeline, ensure that the following tools are installed and ready to use:
- **Apache Airflow**
   - *Check Installation:*  
     ```bash
     airflow version
- **MySQL**
   - *Check Installation:*
     ```bash
     mysql --version
- **PostgreSQL**
   - *Check Installation:*
     ```bash
     psql --version
- **Python**
   - *Check Installation:*  
     ```bash
     python --version
     
If not installed, please refer to the Resources section below for installation instructions and complete the required setup

## Airflow : 

 - Data Pipeline Code : [Dag_script](ecommerce_pipeline.py)
 
 - Dag : ![Graph](Dag_Graph.JPG)

 - Required Airflow and python packages :

    - apache-airflow-providers-common-sql
    - postgresql-16-mysql-fdw (for version 16)
    - apache-airflow-providers-postgres
    - apache-airflow-providers-mysql
    - pandas
      
 - Required Connections : [Airflow_Instructions](Airflow_Connections.docx)

## Environment setup : 

Kindly refer to the instructions below and complete the required setup to initialize the data pipeline.

 - [Instructions](Linux_Environment_Setup.docx)

## Challenges & Solutions :

During the development of this data pipeline, several challenges were encountered. Kindly refer to the document below for common issues and their solutions.

 - [Details](Common_Issues.docx)

## Resources & Downloads

Below are the official download links for the tools used in this project:

- **Apache Airflow**
  - *Installation Guide*: [https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)
  - *GitHub Repository*: [https://github.com/apache/airflow](https://github.com/apache/airflow)

- **MySQL**
  - *Download MySQL*: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
  - *Official Documentation*: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)

- **PostgreSQL**
  - *Download PostgreSQL*: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
  - *Official Documentation*: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

- **MySQL FDW for PostgreSQL**
  - *Installation Guide*: [https://wiki.postgresql.org/wiki/Foreign_data_wrappers#MySQL](https://wiki.postgresql.org/wiki/Foreign_data_wrappers#MySQL)

- **pgAdmin 4 (PostgreSQL Management Tool)**
  - *Download pgAdmin*: [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/)

- **Python**
  - *Download Python*: [https://www.python.org/downloads/](https://www.python.org/downloads/)

- **Pandas (Python Library for Data Processing)**
   - *Installation Guide*: [https://pandas.pydata.org/docs/getting_started/install.html](https://pandas.pydata.org/docs/getting_started/install.html)
     
- **Lucidchart (For Diagram Creation)**
   - *Lucidchart Website*: [https://www.lucidchart.com/](https://www.lucidchart.com/)
---

## About Me  

I am a passionate **Data Engineer** with expertise in **SQL, Python, Apache Airflow, PostgreSQL, MySQL, and Big Data technologies**.  
I have built **scalable data pipelines** for efficient data processing and transformation.  

**Skills:** Linux/Shell | SQL | Python | Apache Airflow | PostgreSQL | MySQL | Apache Spark | Kafka  
**Career Goal:** To work as a **Data Engineer** and contribute to designing robust data architectures.  

📧 **Email:** elokesh4292@gmail.com  
🔗 **LinkedIn:** [Profile](https://www.linkedin.com/in/eegapuri-lokeshwar-reddy-281327308)  

