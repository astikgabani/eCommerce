from app import app

from models.users import UserModel, UserRoleModel

from plugins.admin import admin
from plugins.api import api
from plugins.db import db
from plugins.ma import ma
from plugins.mail import mail

from add_resources import add_resources
from add_admin_views import add_admin_views

admin.init_app(app)
api.init_app(api)
db.init_app(app)
ma.init_app(app)
mail.init_app(app)


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


add_resources(api)
add_admin_views(admin)

if __name__ == "__main__":
    app.run(port=7000)
