

from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.orm import Session
from src.schemas.taxis import TripData
from  math import sin, cos, pi
from dependencies import getdb
from src.models.taxi import taxis_table
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
router= APIRouter(
    prefix="/predict",
    tags= ["predict"]
)
spark= SparkSession.builder.appName("jsonToPyspark").getOrCreate()

@router.post('/')
def predict(taxi: TripData, db: Session= Depends(getdb)):
 angle_hour = 2 * pi / 24
 angle_day = 2 * pi / 7
 angle_month = 2 * pi / 12

 pickup_dt=taxi.tpep_pickup_datetime
 dropoff_dt= taxi.tpep_dropoff_datetime

 dure_trajet= (dropoff_dt - pickup_dt).total_seconds()/60
 # add this data to db
 taxi_db  = {
         "VendorID": taxi.VendorID,
        "tpep_pickup_datetime": taxi.tpep_pickup_datetime,
        "tpep_dropoff_datetime": taxi.tpep_dropoff_datetime,
        "passenger_count": taxi.passenger_count,
        "trip_distance": taxi.trip_distance,
        "RatecodeID": taxi.RatecodeID,
        "store_and_fwd_flag": taxi.store_and_fwd_flag,
        "PULocationID": taxi.PULocationID,
        "DOLocationID": taxi.DOLocationID,
        "payment_type": taxi.payment_type,
        "fare_amount": taxi.fare_amount,
        "extra": taxi.extra,
        "mta_tax": taxi.mta_tax,
        "tip_amount": taxi.tip_amount,
        "tolls_amount": taxi.tolls_amount,
        "improvement_surcharge": taxi.improvement_surcharge,
        "total_amount": taxi.total_amount,
        "congestion_surcharge": taxi.congestion_surcharge,
        "Airport_fee": taxi.Airport_fee,
        "cbd_congestion_fee": taxi.cbd_congestion_fee,
        "dure_trajet": dure_trajet
    }
 

 data_insert= insert(taxis_table).values(**taxi_db)
 db.execute(data_insert)
 db.commit()
 #create the model data
 pickup_dt = taxi.tpep_pickup_datetime
 dropoff_dt = taxi.tpep_dropoff_datetime
 pickup_hour = pickup_dt.hour
 pickup_dayofweek = pickup_dt.isoweekday()  # 1 = Monday, 7 = Sunday
 pickup_month = pickup_dt.month

 dropoff_hour = dropoff_dt.hour
 dropoff_dayofweek = dropoff_dt.isoweekday()
 dropoff_month = dropoff_dt.month

 pickup_hour_sin = sin(pickup_hour * angle_hour)
 pickup_hour_cos = cos(pickup_hour * angle_hour)
 pickup_dayofweek_sin = sin((pickup_dayofweek - 1) * angle_day)
 pickup_dayofweek_cos = cos((pickup_dayofweek - 1) * angle_day)
 pickup_month_sin = sin((pickup_month - 1) * angle_month)
 pickup_month_cos = cos((pickup_month - 1) * angle_month)

 dropoff_hour_sin = sin(dropoff_hour * angle_hour)
 dropoff_hour_cos = cos(dropoff_hour * angle_hour)
 dropoff_dayofweek_sin = sin((dropoff_dayofweek - 1) * angle_day)
 dropoff_dayofweek_cos = cos((dropoff_dayofweek - 1) * angle_day)
 dropoff_month_sin = sin((dropoff_month - 1) * angle_month)
 dropoff_month_cos = cos((dropoff_month - 1) * angle_month)

 data= [{
    "VendorID": taxi.VendorID,
    "passenger_count": taxi.passenger_count ,
    "trip_distance": taxi.trip_distance,
    "RatecodeID": taxi.RatecodeID,
    "DOLocationID": taxi.DOLocationID,
    "payment_type": taxi.payment_type,
    "tip_amount": taxi.tip_amount,
    "tolls_amount": taxi.tolls_amount,
    "congestion_surcharge": taxi.congestion_surcharge,
    "Airport_fee": taxi.Airport_fee,
    "pickup_hour_sin": pickup_hour_sin,
    "pickup_hour_cos": pickup_hour_cos,
    "pickup_dayofweek_sin": pickup_dayofweek_sin,
    "pickup_dayofweek_cos": pickup_dayofweek_cos,
    "pickup_month_sin": pickup_month_sin,
    "pickup_month_cos": pickup_month_cos,
    "dropoff_hour_sin": dropoff_hour_sin,
    "dropoff_hour_cos": dropoff_hour_cos,
    "dropoff_dayofweek_sin": dropoff_dayofweek_sin,
    "dropoff_dayofweek_cos": dropoff_dayofweek_cos,
    "dropoff_month_sin": dropoff_month_sin,
    "dropoff_month_cos": dropoff_month_cos,
}]
# Calculate dure_trajet in minutes
 df= spark.createDataFrame(data)
 model_path='/home/hp/simplon_projects/duree_trajet/data/gold/saved_model'
 model= PipelineModel(model_path)
 result= model.transform(df)
 return {"status": "ok", "dure_trajet": dure_trajet}
