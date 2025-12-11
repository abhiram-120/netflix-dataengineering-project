# Netflix End-to-End Data Engineering Project

## Overview
This project is a complete end-to-end data engineering solution for Netflix content analysis, leveraging Azure Data Services and Databricks. This solution establishes a robust data processing pipeline featuring parameterized notebooks, streaming Delta Live Tables (DLT), and optimized job orchestration—all crucial for analytical reporting, data warehousing, and advanced model building.

The pipeline begins by fetching necessary raw data from GitHub, which is then processed through an Azure Data Factory pipeline. This initial stage includes essential validations before successfully storing the data in designated Azure Data Lake containers.

## Architecture: Medallion Lakehouse Approach 
The project adheres to the Medallion Architecture (Bronze, Silver, Gold layers), an efficient and scalable approach to progressively refine data quality and structure:
- Bronze Layer (Raw): Landing zone for raw, untransformed data.
- Silver Layer (Cleaned & Conformed): Data is cleansed, validated, and structured, forming an enterprise view.
- Gold Layer (Curated & Optimized): Final, highly curated data models tailored for direct consumption by BI tools and analytical applications.
This architectural choice ensures step-by-step data processing, enhancing data quality and reliability throughout the pipeline.
<img src="Architecture Diagram.jpg">


## Detailed Data Flow & Processing Steps 
Once data resides in the Azure Data Lake, Databricks is leveraged for all subsequent processing, including transformations, streaming, and quality enforcement within a Unity Catalog environment.<br>

**1. Azure Data Factory Ingestion & Orchestration:**
   - Data Ingestion: Fetches raw data from GitHub sources.
   - Initial Validation & Storage: Performs necessary initial validations and then successfully lands the data into specific Azure Data Lake containers (e.g., raw).
   - Orchestration: Manages the overall pipeline flow, ensuring sequential execution of notebooks and DLT pipelines.
     
<img src="Screenshots/adf_pipeline.png">

**2. Databricks Bronze Layer (Automated Ingestion):**
  - Databricks Autoloader: Seamlessly pushes incremental data from the raw container into the Bronze Layer. This provides an automated, scalable, and schema-evolving loading process for the netflix_titles dataset.
Output: Data is stored as Delta tables in abfss://bronze@netflixprojectdl.dfs.core.windows.net/netflix_titles.
<img src="Screenshots/1_autoloader.png"> 

**3. Databricks Silver Layer (Transformation & Refinement):**
  - Parameterized Notebooks: Utilized for processing various lookup tables (e.g., directors, cast, countries, categories). These notebooks use dynamic inputs (e.g., sourcefolder, targetfolder) via a job pipeline to efficiently process and write data into the Silver Layer.
  - Data Transformations: Performs crucial transformations including:
     - Eliminating null values.
     - Correcting data formats and content.
     - Refining the overall schema to a clean, conformed state.
Output: Cleaned and transformed data is stored as Delta tables in abfss://silver@netflixprojectdl.dfs.core.windows.net/netflix_titles and other lookup tables (e.g., silver/netflix_directors).
<img src="Screenshots/3_silver_lookup_pipeline.png"> <br>

**4. Databricks Job Orchestration with Conditional Execution:**
  - Implemented advanced workflow control for Silver layer processing, leveraging dbutils.jobs.taskValues for inter-task communication.
  - A dedicated WeekdayLookup task dynamically determined the current day of the week, passing this value as a task output.
  - An If/Else condition task then evaluated this output, enabling conditional execution of downstream Silver layer notebooks. This allowed specific processing (e.g., silver Master Data transformations) to run only on designated days (e.g., Sundays), with an alternative path (FalseNotebook) executing on other days for controlled pipeline behavior.
<img src="Screenshots/5_silver_data%20pipeline_run.png"> <br> 

**5. Databricks Gold Layer (Curated & Validated with DLT):**
  - Delta Live Tables (DLT) Pipeline: The heart of the Gold layer, automating the creation and management of reliable data pipelines.
  - Data Quality Constraints: A set of predefined rules (constraints) are applied (expect_all_or_drop and expect_or_drop) to purify the overall data. These rules ensure data integrity and consistency, dropping records that fail validation.
  - Final Data Models: Successfully processes the cleansed data, creating Delta Live Tables in the Gold layer (e.g., gold_netflixtitles, gold_netflixdirectors, etc.). These tables are now fully cleansed, validated, and optimized for consumption.
Output: Consumption-ready Delta tables in the gold layer, ready for downstream applications.
<img src="Screenshots/7_DeltaLiveTable_Pipeline_run.png">

**6. Reporting & Warehousing Integration:**
- Data from the Gold layer was integrated with Power BI to construct a dynamic and insightful dashboard. 
<img src="Netflix Dashboard.png">

## Data Governance & Security with Unity Catalog 
The entire Databricks workspace was integrated with the Unity Catalog environment, a pivotal component for centralized data governance. This robust integration offered:
- Centralized Metadata Management: Facilitated data processing without the creation of data duplications, ensuring a single source of truth.
- Database Catalog Integration: Enabled the structured storage of tables and schemas directly within the database catalog.
- Secure Metastore: Stored all metadata within the existing Metastore, establishing a secure and governed framework for data engineering operations.
  
## 🛠️Skills Gained & Technologies Utilized
This project effectively utilizes the following Azure services:
-  Azure Data Factory (ADF) – Seamless data orchestration
-  Databricks – Smarter data processing with Spark
- Unity Catalog – Secure and scalable data governance
-  Delta Live Tables (DLT) – Automated pipeline magic
-  Apache Spark – Power behind big data processing
-  Delta Lake – Reliable & fast data lakehouse
-  Azure Data Lake – Scalable cloud storage
-  Power BI – Interactive dashboards & insightful reporting

##Dataset Used
This project utilizes a publicly available dataset sourced from Kaggle, detailing Netflix's extensive catalog of movies and TV shows.

**Link:** [https://www.kaggle.com/datasets/shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**About the Dataset:** <br>
This tabular dataset provides a comprehensive listing of movies and TV shows available on the Netflix platform. Sourced as of mid-2021, it captures key attributes for over 8000 titles, offering insights into content characteristics such as cast, directors, content ratings, release year, and duration. This rich metadata serves as the foundational input for the analytical pipeline.


