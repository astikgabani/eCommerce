import os

DEBUG = True
ENV = "development"
TESTING = True
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "asdasdasd")
SECRET_KEY = os.environ.get("APP_SECRET_KEY", "asdasdasd")
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
