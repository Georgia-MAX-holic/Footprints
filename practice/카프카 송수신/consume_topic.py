#consume_topic.py

from pyspark.sql import SparkSession

sc = SparkSession.builder.getOrCreate()

sc.sparkContext.setLogLevel('ERROR')

# Read 
log = sc.readStream.format("kafka") \
.option("kafka.bootstrap.servers", "kafka-1:19092") \
.option("subscribe", "test1") \
.option("startingOffsets", "earliest") \
.load()

# Write 
query = log.selectExpr("CAST(value AS STRING)") \
.writeStream \
.format("console") \
.option("truncate", "false") \
.start()

# HDFS
query2 = log.selectExpr("CAST(value AS STRING)") \
.writeStream \
.format("csv") \
.outputMode("append") \
.option("checkpointLocation", "/check") \
.option("path", "/luka2") \
.start()

query.awaitTermination()
query2.awaitTermination()
        