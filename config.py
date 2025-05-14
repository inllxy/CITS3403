# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "replace-with-random-string"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "sf6_spotlight.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
