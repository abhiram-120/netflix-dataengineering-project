NETFLIX - END TO END DATAENGINEERING PROJECT 

Update

To briefly sum it up, it fetches the necessary data from GitHub and processes necessary validations using the Azure data factory pipeline successfully storing it in the required data lake containers. I have divided the layers into bronze, silver and gold in the architecture, which is an efficient approach on how we can process data step by step. Ones the data is the data lake, it is given access to Databricks where we can perform the further steps as transformation, streaming etc. I have added my workspace the Unity catalog environment where it allows me to perform data processing without creating any duplications and enables storing the tables, schema in the database catalog along with storing it s metadata in the existing Metastore, making it secure means of data engineering. With help of the autoloader, it seamless pushed the data from the raw layer to the bronze layer enabling an automation loading process.

After being successfully loaded into the bronze layer, before sending the data into the silver layer, parameterized notebooks is being created in order to make the processing more efficient, where with the help of lookup inputs using a pipeline, processes the data and write it into the silver layer, after performing the required transformations as eliminating null values, and correcting formats, contents and refining the overall schema.

Ones it approaches the gold layer, I proceeded in creating the delta live table pipeline, where I created set of rule, so called constraints to purify the overall data and process accordingly. Using the DLT pipeline with a successful validation, I was able to successfully process the data and created the delta live tables which is now fully cleansed further serving takes place where it can use the sql warehouse to successfully integrated with reporting applications as power BI or azure synapse for warehousing, successfully creating an efficient flow of data

Skills gained :

-Delta Live Tables (DLT) -Azure Data Factory Pipelines -Databricks Autoloader -Parameterized Notebooks -Unity Catalog Integration -Streaming Data Processing

This is an end to end project
