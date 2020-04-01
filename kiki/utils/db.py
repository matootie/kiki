"""
Database utilities.
"""

import os
from databases import Database
from databases import DatabaseURL
from sqlalchemy import MetaData


# Establish an instance of the database, and SQLAlchemy metadata
# for use with the ORM.
_PG_H = os.environ["POSTGRES_HOST"]
_PG_U = os.environ["POSTGRES_USER"]
_PG_P = os.environ["POSTGRES_PASS"].rstrip("\n")
_PG_N = os.environ["POSTGRES_NAME"]

_url_string = f"postgresql://{_PG_H}:{_PG_P}@{_PG_H}:5432/{_PG_N}"

_db_url = DatabaseURL(url=_url_string)
database = Database(_db_url)
metadata = MetaData()
