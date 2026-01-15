

from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.orm import Session
from src.schemas.taxis import TripData
from  math import sin, cos, pi
from dependencies import getdb
from src.models.taxi import taxis_table
router= APIRouter(
    prefix="/predict",
    tags= ["predict"]
)

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
 #create the model data
 
 data_insert= insert(taxis_table).values(**taxi_db)
 db.execute(data_insert)
 db.commit()


 return {"status": "ok", "dure_trajet": dure_trajet}
