# Databricks notebook source
# MAGIC %md
# MAGIC # DLT NOTEBOOK - gold layer

# COMMAND ----------

looktables_rules = {

    "rule1" : "show_id is NOT NULL",
    
}

# COMMAND ----------

@dlt.table(

    name = "gold_netlfixdirectors"
)

@dlt.expect_all_or_drop(looktables_rules)
def myfunc():
    df =spark.readStream.format("delta").load("abfss://silver@netflixprojdatastorage.dfs.core.windows.net/netflix_directors")
    return df



# COMMAND ----------

@dlt.table(

    name = "gold_netlfixcast"
)

@dlt.expect_all_or_drop(looktables_rules)

def myfunc():
    df =spark.readStream.format("delta").load("abfss://silver@netflixprojdatastorage.dfs.core.windows.net/netflix_cast")
    return df



# COMMAND ----------

@dlt.table(

    name = "gold_netlfixcountries"
)

@dlt.expect_all_or_drop(looktables_rules)

def myfunc():
    df =spark.readStream.format("delta").load("abfss://silver@netflixprojdatastorage.dfs.core.windows.net/netflix_countries")
    return df



# COMMAND ----------

@dlt.table(

    name = "gold_netlfixcategory"
)

@dlt.expect_all_or_drop(looktables_rules)

def myfunc():
    df =spark.readStream.format("delta").load("abfss://silver@netflixprojdatastorage.dfs.core.windows.net/netflix_category")
    return df


# COMMAND ----------

@dlt.table
def gold_stg_netflixtitles():
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdatastorage.dfs.core.windows.net/netflix_titles")
    return df


# COMMAND ----------


from pyspark.sql.functions import*

# COMMAND ----------

@dlt.view

def gold_trns_netflixtitles(): 
    df = spark.readStream.table("LIVE.gold_stg_netflixtitles")
    df = df.withColumn("newflag",lit("1"))
    return df

# COMMAND ----------

masterdata_rules = {

    "rule1" : "newflag is NOT NULL",
    "rule2" : "show_id is NOT NULL"
}

# COMMAND ----------

@dlt.table

@dlt.expect_all_or_drop(masterdata_rules)
def gold_netflixtitles(): 
    
    df = spark.readStream.table("LIVE.gold_trns_netflixtitles")
    return df 

# COMMAND ----------

dff = spark.read.table("LIVE.gold_trns_netflixtitles")
dff.show(10)