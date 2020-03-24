"""
Database utilities.
"""

import os
from databases import Database
from databases import DatabaseURL
from sqlalchemy import MetaData


# Establish an instance of the database, and SQLAlchemy metadata
# for use with the ORM.
_POSTGRES_HOST = os.environ["POSTGRES_HOST"]
_POSTGRES_USER = os.environ["POSTGRES_USER"]
_POSTGRES_PASS = os.environ["POSTGRES_PASS"]
_POSTGRES_NAME = os.environ["POSTGRES_NAME"]

_url_string = f"postgresql://{_POSTGRES_HOST}:5432/{_POSTGRES_NAME}?user={_POSTGRES_USER}&password={_POSTGRES_PASS}"

_db_url = DatabaseURL(url=_url_string)
database = Database(_db_url)
metadata = MetaData()
