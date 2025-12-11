# Netflix Data Lakehouse: End-to-End Azure Engineering

## Project Overview
This project demonstrates an enterprise-grade Data Lakehouse architecture built on Azure and Databricks. It is designed to handle high-volume data ingestion, transformation, and governance using the Medallion Architecture.

Unlike standard pipelines that just move data, this project focuses on Data Quality enforcement, Schema Evolution, and Cost Optimization using Auto Loader.

---

## Architecture
**Design Pattern:** Medallion Architecture (Lakehouse)
*   **Bronze Layer:** Raw data ingestion (Append-Only).
*   **Silver Layer:** Cleaned, validated, and enriched data (Upserts/Merge).
*   **Gold Layer:** Aggregated business-level tables for BI (Star Schema).

**Why Medallion?**
I chose Medallion over a traditional Monolithic warehouse because it allows for "Time Travel" debugging. If the Silver transformation fails, the Bronze data remains intact, allowing for data replay without re-ingesting from the source.

<img src="Architecture Diagram.jpg" width="800">

---

## Technical Implementation & Design Decisions

### 1. Ingestion via Databricks Auto Loader
Replaced traditional bulk loads (Copy Activity) with Databricks Auto Loader (`cloudFiles`).

**Why Auto Loader?**
Traditional `COPY INTO` commands require listing all files in the storage bucket, which becomes slow as the dataset grows to millions of files. Auto Loader uses event notifications (Event Grid) to process only new files, keeping ingestion costs flat regardless of data volume.

<img src="Screenshots/1_autoloader.png" width="600">

### 2. Transformation Layer (PySpark & Silver)
Created parameterized notebooks that accept `source_path` and `table_name` as widgets.

**Why Parameterization?**
Hardcoding table names creates tech debt. By parameterizing the logic, I reduced 10 separate notebooks (one for each table) into a single generic notebook, reducing code maintenance by 90%.

<img src="Screenshots/3_silver_lookup_pipeline.png" width="600">

### 3. Workflow Orchestration with Conditional Logic
Configured Databricks Workflows with `dbutils.jobs.taskValues` to pass execution states between tasks.

**Why Conditional Execution?**
Full pipeline runs are expensive. By adding conditional checks (e.g., checking if source data arrived), I prevent the heavy Spark clusters from spinning up unnecessarily, optimizing compute costs.

<img src="Screenshots/5_silver_data%20pipeline_run.png" width="600">

### 4. Quality Assurance (Delta Live Tables - DLT)
Deployed DLT Pipelines for the Gold Layer with `expect_or_drop` constraints.

**Why DLT?**
In standard Spark, writing data quality checks requires complex boilerplate code. DLT treats Data Quality as a configuration. It automatically quarantines bad data, ensuring the BI dashboard never breaks due to a schema mismatch or null primary key.

<img src="Screenshots/7_DeltaLiveTable_Pipeline_run.png" width="600">

---

## Data Governance (Unity Catalog)
Integrated the workspace with Unity Catalog to replace the legacy Hive Metastore.

**Why Unity Catalog?**
The biggest bottleneck in AI/Analytics is security. Unity Catalog decouples permissions from the physical storage path. This means I can grant access to a specific *table* without giving a user read access to the entire *storage container*.

---

## Tech Stack
*   **Cloud:** Microsoft Azure (ADLS Gen2, ADF)
*   **Compute:** Azure Databricks (Spark 3.4)
*   **Language:** Python (PySpark), SQL
*   **Format:** Delta Lake
*   **DevOps:** Git Integration

## Dataset
**Source:** [Kaggle - Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
