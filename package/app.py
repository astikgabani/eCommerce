from logging.config import fileConfig, dictConfig
from urllib.parse import urljoin

from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import configure_uploads, patch_request_class
from flask_jwt_extended import JWTManager
from flask_login import login_user, logout_user, LoginManager, current_user

from models.users import UserModel

from dotenv import load_dotenv
from marshmallow import ValidationError

from utils.image_helper import IMAGE_SET

from constants.constants import get_path

import werkzeug.exceptions


app = Flask(__name__)

# Logging Configuration
from config.logging import log_config

dictConfig(log_config)

load_dotenv(get_path("config", ".env"), verbose=True)
app.config.from_object("config.default_config")
app.config.from_object("config.mail_config")
# app.config.from_object("config.production_config")

patch_request_class(app, 10 * 1024 * 1024)  # 10 MB Max

configure_uploads(app, IMAGE_SET)
jwt = JWTManager(app)
login_manager = LoginManager(app)


@app.errorhandler(ValidationError)
def validation_error(error):
    return error.messages, 400


@app.errorhandler(429)
def rate_limit_handler(error):
    return {"message": "rate limit exceeded %s" % error.description}, 429


@app.errorhandler(AssertionError)
def validation_error(error):
    return {"Error": str(error)}, 400


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get_item(id=int(user_id))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    app.logger.error("starting the admin page")
    redirect_path = request.args.get("next") or request.form.get("next") or None
    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        error = "Invalid Credentials"
        status = "danger"
        if not (email and password):
            error = "Email or password not provided"
        else:
            user = UserModel.get_item(email=email)
            if user and user.verify_password(password):
                if "admin" in (role.role for role in user.roles):
                    login_user(user)
                    return redirect(
                        urljoin(request.host_url, redirect_path)
                        if redirect_path
                        else url_for("admin.index")
                    )
                error = "Admin role is required"
        return render_template("login.html", error=error, status=status)
    return render_template("login.html")


@app.route("/admin-logout")
def admin_logout():
    if current_user:
        logout_user()
    return render_template("login.html", status="success", error="Logout Successfully")
