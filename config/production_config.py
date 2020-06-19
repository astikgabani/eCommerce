import os

DEBUG = False
ENV = "production"
TESTING = False
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
