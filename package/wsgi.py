from app import app

from flask_restful import Api

from models.users import UserModel, UserRoleModel

from plugins.admin import admin
from plugins.db import db
from plugins.ma import ma
from plugins.mail import mail
from plugins.limiter import limiter

from add_resources import add_resources
from add_admin_views import add_admin_views

db.init_app(app)
ma.init_app(app)
mail.init_app(app)
admin.init_app(app)
limiter.init_app(app)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    if UserRoleModel.get_item(role="admin"):
        return
    user_role = UserRoleModel()
    user_role.role = "admin"
    user_role.save_to_db()
    user = UserModel()
    user.email = "admin@example.com"
    user.password = "admin"
    user.first_name = "admin"
    user.last_name = "admin"
    user.phone_no = 9999999999
    user.save_to_db()
    user.roles.append(user_role)
    user.save_to_db()


add_resources(api)
add_admin_views(admin)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
