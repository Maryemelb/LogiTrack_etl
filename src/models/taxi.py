import sqlalchemy

from src.db.database import Base
from sqlalchemy import Column, Integer, Float, DateTime, String, Table, MetaData



# use SQLAlchemy core
metadata= MetaData()
taxis_table = Table(
    "taxis", metadata,
    Column("VendorID", Integer),
    Column("tpep_pickup_datetime", DateTime),
    Column("tpep_dropoff_datetime", DateTime),
    Column("passenger_count", Integer),
    Column("trip_distance", Float),
    Column("RatecodeID", Integer),
    Column("store_and_fwd_flag", String),
    Column("PULocationID", Integer),
    Column("DOLocationID", Integer),
    Column("payment_type", Integer),
    Column("fare_amount", Float),
    Column("extra", Float),
    Column("mta_tax", Float),
    Column("tip_amount", Float),
    Column("tolls_amount", Float),
    Column("improvement_surcharge", Float),
    Column("total_amount", Float),
    Column("congestion_surcharge", Float),
    Column("Airport_fee", Float),
    Column("cbd_congestion_fee", Float),
    Column("dure_trajet", Float)
)