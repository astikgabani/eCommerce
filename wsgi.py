from app import app as application

from models.users import UserModel, UserRoleModel

from plugins.db import db
from plugins.ma import ma
from plugins.mail import mail
from plugins.admin import admin


db.init_app(application)
ma.init_app(application)
mail.init_app(application)
admin.init_app(application)


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


if __name__ == "__main__":
    application.run()
