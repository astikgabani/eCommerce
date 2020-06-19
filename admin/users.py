from admin.helper.helper import SuperView

from models.users import (
    UserModel,
    UserRoleModel,
    UserSessionModel,
    UserConfirmationModel,
    UserSessionTokenModel,
)
from models.address import AddressModel
from models.cart import CartModel


class UserView(SuperView):

    inline_models = [
        AddressModel,
        UserRoleModel,
        UserSessionModel,
        UserConfirmationModel,
        CartModel,
    ]
    column_exclude_list = ["password"]
    column_filters = ("email",)

    column_searchable_list = ("email", "phone_no")

    def __init__(self, model=UserModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class UserRoleView(SuperView):

    column_filters = ("role",)

    column_searchable_list = ("role",)

    def __init__(self, model=UserRoleModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class UserSessionView(SuperView):
    inline_models = [UserSessionTokenModel]

    column_filters = ("ip", "type")

    column_searchable_list = ("ip", "type")

    def __init__(self, model=UserSessionModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class UserSessionTokenView(SuperView):
    # inline_models = [UserSessionModel]

    def __init__(self, model=UserSessionTokenModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class UserConfirmationView(SuperView):
    # inline_models = [UserModel]

    def __init__(self, model=UserConfirmationModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
