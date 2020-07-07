from marshmallow import RAISE, EXCLUDE
from plugins.ma import ma

from models.cart import CartModel, CartItemsModel


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id", "total")
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItemsModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = EXCLUDE
        load_instance = True
