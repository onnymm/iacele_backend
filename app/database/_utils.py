import os
import json
from urllib.parse import quote_plus
from typing import Literal

def create_db_url():
    url = os.environ.get("PG_DB_URL")
    port = os.environ.get("PG_DB_PORT")
    name = os.environ.get("PG_DB_NAME")
    username = os.environ.get("PG_DB_USERNAME")
    password = os.environ.get("PG_DB_PASSWORD")

    username = quote_plus(username)
    password = quote_plus(password)


    return f"postgresql+psycopg2://{username}:{password}@{url}:{port}/{name}"
