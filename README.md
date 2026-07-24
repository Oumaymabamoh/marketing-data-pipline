# End-to-End E-Commerce Data Pipeline & Analytics

An automated, end-to-end modern data stack pipeline that ingests raw e-commerce marketing data, transforms it using dbt, orchestrates execution daily with Apache Airflow, and serves real-time executive insights via a Streamlit dashboard.

## 🏗 Architecture

## 🛠 Tech Stack
- Orchestration: Apache Airflow
- Data Transformation: dbt (data build tool)
- Database / Analytical Storage: DuckDB
- Visualization: Streamlit & Plotly
- Language: Python 3.x

## 🚀 Key Features
- Automated Data Ingestion: PySpark / Python script populates raw transactional and ad-spend data into DuckDB.
- Modular dbt Modeling: Cleans, aggregates, and transforms raw data into a production-ready fact table (fct_daily_marketing_performance).
- Scheduled Pipeline: Airflow DAG (ecommerce_daily_pipeline) executes daily ingestion and transformation tasks sequentially.
- Interactive Dashboard: Live KPIs, ROAS (Return on Ad Spend) analysis, and daily revenue vs. ad-spend trends by channel.

## 🚦 Getting Started
nsure you have Python 3.9+ installed and clone this repository:
### 1. Prerequisites
### 2. Install Dependencies
### 3. Run Airflow Standalone
### 4. Launch the Dashboard

## 📈 Dashboard Preview
