"""
Database utilities.
"""

import os
from databases import Database
from databases import DatabaseURL
from sqlalchemy import MetaData


# Establish an instance of the database, and SQLAlchemy metadata
# for use with the ORM.
_db_url = DatabaseURL(os.environ["DATABASE_URL"])
database = Database(_db_url)
metadata = MetaData()
