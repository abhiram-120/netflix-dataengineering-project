# Databricks notebook source
dbutils.widgets.text("weekday", "7")

# COMMAND ----------


weekday_value = dbutils.widgets.get("weekday")
var = int(weekday_value)


# COMMAND ----------

dbutils.jobs.taskValues.set(key="weekoutput", value = var)