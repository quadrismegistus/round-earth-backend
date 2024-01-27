import os
from functools import lru_cache as cache, cached_property
from typing import *
# from fastapi import FastAPI
# from sqlmodel import Field, Session, SQLModel, create_engine, select, Column
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text as sql_text
from geopy.distance import geodesic
from shapely import wkb
import itertools
from sqlalchemy import and_

PATH_DATA = os.path.expanduser('~/.cache/round-earth-backend')
PATH_REPO = os.path.dirname(os.path.dirname(__file__))

PATHS_SPATIALITE = ['/opt/homebrew/lib/mod_spatialite.dylib']

DB_USERNAME = 'postgres'
DB_DATABASE = 'round_earth'
DB_HOST = 'localhost'
DB_CLEAR = True

from .utils import *
