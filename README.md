# 🕷️ Job Scraper with Airflow & Docker

A modular, production-ready data pipeline for scraping job offers using **Selenium**, orchestrated with **Apache Airflow**, and containerized with **Docker**. The data is stored in **PostgreSQL**.

---

## 🚀 Features

- 🔄 **Daily scraping DAG** managed by Airflow
- 🐳 Fully containerized via **Docker Compose**
- 🌐 Uses headless **Chromium** + **ChromeDriver**
- 💾 Persists job offers in a **PostgreSQL** database

---

## ⚙️ Services (via Docker Compose)

| Service          | Description                                       |
|------------------|---------------------------------------------------|
| `db`             | PostgreSQL database for storing scraped data     |
| `airflow_db`     | PostgreSQL backend for Airflow metadata          |
| `airflow-webserver` | Web UI for managing DAGs                    |
| `airflow-scheduler` | Executes and manages DAG schedules          |
| `airflow-init`   | Initializes Airflow metadata + admin user        |
| `scraper`        | Standalone scraping container invoked by Airflow |



