import psycopg2
from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

# Database connection parameters
db_params = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
}

# Function to get the database version
def get_db_version():
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                return version[0]  # Returns the version string
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db-version")
def read_db_version():
    version = get_db_version()
    return {"PostgreSQL Version": version}
