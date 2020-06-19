from urllib.parse import urljoin

from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api
from flask_uploads import configure_uploads, patch_request_class
from flask_jwt_extended import JWTManager
from flask_login import login_user, logout_user, LoginManager, current_user

from models.users import UserModel, UserRoleModel

from dotenv import load_dotenv
from marshmallow import ValidationError

from plugins.admin import admin
from plugins.db import db
from plugins.ma import ma
from plugins.mail import mail

from add_resources import add_resources
from add_admin_views import add_admin_views

from utils.image_helper import IMAGE_SET


app = Flask(__name__)

load_dotenv("config/.env", verbose=True)
app.config.from_object("config.default_config")
app.config.from_object("config.mail_config")
# app.config.from_object("config.production_config")

patch_request_class(app, 10 * 1024 * 1024)  # 10 MB Max

configure_uploads(app, IMAGE_SET)
api = Api(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)


@app.errorhandler(ValidationError)
def validation_error(error):
    return error.messages, 400


@app.errorhandler(AssertionError)
def validation_error(error):
    return {"Error": str(error)}, 400


@app.before_first_request
def create_tables():
    db.create_all()
    if UserRoleModel.get_item(role="admin"):
        return
    user_role = UserRoleModel()
    user_role.role = "admin"
    user_role.save_to_db()
    user = UserModel()
    user.email = "admin_test@yopmail.com"
    user.password = "admin123"
    user.first_name = "admin"
    user.last_name = "admin"
    user.phone_no = 9999999999
    user.save_to_db()
    user.roles.append(user_role)
    user.save_to_db()


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get_item(id=int(user_id))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
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


add_resources(api)
add_admin_views(admin)


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    app.run(port=7000)
