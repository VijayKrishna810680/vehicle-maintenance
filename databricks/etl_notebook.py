# Databricks-style ETL notebook (Python)
# Steps:
# 1. Load raw CSV from cloud storage
# 2. Bronze: store raw parquet
# 3. Silver: clean and normalize
# 4. Gold: aggregate for analytics

import pyspark.sql.functions as F

# Example paths (replace with your storage paths)
raw_path = '/mnt/raw/vehicle_maintenance/*.csv'
bronze_path = '/mnt/bronze/vehicle'
silver_path = '/mnt/silver/vehicle'
gold_path = '/mnt/gold/vehicle_agg'

# 1. Read raw
df_raw = spark.read.option('header', True).csv(raw_path)

# 2. Bronze - write raw parquet
df_raw.write.mode('overwrite').parquet(bronze_path)

# 3. Silver - simple cleaning
df_silver = df_raw.withColumn('year', F.col('year').cast('int'))                           .withColumn('vin', F.trim(F.col('vin')))                           .dropna(subset=['vin'])

df_silver.write.mode('overwrite').parquet(silver_path)

# 4. Gold - example aggregation: count records per make
df_gold = df_silver.groupBy('make').count().orderBy(F.desc('count'))
df_gold.write.mode('overwrite').parquet(gold_path)

display(df_gold)
