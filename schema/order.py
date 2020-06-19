from marshmallow import RAISE, EXCLUDE
from marshmallow_enum import EnumField

from plugins.ma import ma

from models.order import OrderModel, OrderReceiverModel, OrderStatusEnum


class OrderSchema(ma.SQLAlchemyAutoSchema):
    status = EnumField(OrderStatusEnum, by_name=True)

    class Meta:
        model = OrderModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id", "total")
        exclude = ("created", "updated", "active")
        unknown = EXCLUDE
        load_instance = True


class OrderReceiverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderReceiverModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True
