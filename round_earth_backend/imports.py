import os
from functools import lru_cache as cache
from typing import Optional
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

PATH_DATA = os.path.expanduser('~/round_earth_backend_data')
