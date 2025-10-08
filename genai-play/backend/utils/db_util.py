import psycopg2
import json
from settings import Settings


settings = Settings()
conn_params = {
    "dbname": settings.db_name,
    "user": settings.db_user,
    "password": settings.db_password,
    "host": settings.db_host,
    "port": settings.db_port
}

def get_db_connection_from_settings():
    """Return a new PostgreSQL database connection using settings.py."""
    return psycopg2.connect(**conn_params)

