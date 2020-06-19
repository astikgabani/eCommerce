from marshmallow import RAISE, pre_load, INCLUDE, EXCLUDE
from marshmallow_enum import EnumField

from plugins.ma import ma

from models.users import (
    UserModel,
    UserSessionModel,
    GenderEnum,
    SessionEnum,
    UserSessionTokenModel,
    UserRoleModel,
    UserConfirmationModel,
)


class UserSchema(ma.SQLAlchemyAutoSchema):
    gender = EnumField(GenderEnum, by_name=True)

    class Meta:
        model = UserModel
        dateformat = "%d-%m-%Y"
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    type = EnumField(SessionEnum, by_name=True)

    class Meta:
        model = UserModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        fields = ("id", "email", "password")
        load_only = ("password",)
        dump_only = ("id", "confirmed")
        unknown = EXCLUDE
        load_instance = True

    @pre_load
    def slugify_name(self, in_data, **kwargs):
        in_data["clear_input_password"] = in_data.get("password", None)
        in_data.pop("password", None)
        return in_data


class UserSessionSchema(ma.SQLAlchemyAutoSchema):
    type = EnumField(SessionEnum, by_name=True)

    class Meta:
        model = UserSessionModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = INCLUDE
        load_instance = True


class UserSessionTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSessionTokenModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = INCLUDE
        load_instance = True


class UserRoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserRoleModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = EXCLUDE
        load_instance = True


class UserConfirmationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserConfirmationModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        load_only = ("user",)
        unknown = EXCLUDE
        load_instance = True
