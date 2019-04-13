from psycopg2 import connect
from src.constants import *

def connectDB():
    return connect(dbname=DB_NAME,
                   user=DB_USER,
                   password=DB_PASS,
                   host=DB_HOST,
                   port=DB_PORT)