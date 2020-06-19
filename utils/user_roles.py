from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models.users import UserModel, UserRoleModel

ADMIN_ROLE = "admin"


def required_role(roles):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserModel.get_item(id=user_id)
            for role_name in roles:
                role = UserRoleModel.get_item(role=role_name)
                if role in user.roles:
                    return func(*args, **kwargs)
            return {"message": "Not a authorised user"}, 401

        return decorated_function

    return decorator


roles_json = {"UserRoleAssign": {"post": [ADMIN_ROLE]}}
