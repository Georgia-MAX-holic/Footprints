
from pyspark.sql import SparkSession

from category_encoders import OneHotEncoder

spark=SparkSession.builder.appName("R6_study").getOrCreate()

path = 'C:\spark\R6.csv'

df_spark=spark.read.option("header","true").csv(path, inferSchema=True)

class spark :
  
  def __init__(self, df):   
    self.df = df

  def make_ratio_Column(self , name: str , numerator:float , denominator:float):

    self.df = self.df.withColumn(name, (self.df[numerator]/ self.df[denominator]).cast("float"))
    return self.df


def outlier(luka):
    global df
    q1=df[luka].quantile(0.25)
    q2=df[luka].quantile(0.5)
    q3=df[luka].quantile(0.75)
    iqr=q3-q1
    condition=df[luka]>q3+1.5*iqr
    df=df[condition].dropna()
    return df


define = spark(df_spark)


df_spark=define.make_ratio_Column('k/d_ratio','nbkills' ,"nbdeaths") 
df_spark=define.make_ratio_Column('win_ratio','nbkills','nbpicks').dropna()

use_list= ["role","operator","primaryweapon","secondaryweapon","nbwins", "nbkills","nbdeaths","nbpicks",'win_ratio','k/d_ratio']

df_spark=df_spark.select(use_list)

df = df_spark.toPandas()


# outlier 함수를 통하여 각 값의 이상치 여부를 찾고 새로운 열에 결과 저장
outlier("win_ratio")
outlier("k/d_ratio")


df.to_csv('./outlier.csv')


