from marshmallow import RAISE, EXCLUDE, fields
from marshmallow_enum import EnumField

from plugins.ma import ma

from models.order import (
    OrderModel,
    OrderReceiverModel,
    OrderStatusEnum,
    PaymentStatusEnum,
)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    status = EnumField(OrderStatusEnum, by_name=True)
    payment_status = EnumField(PaymentStatusEnum, by_name=True)
    user_id = fields.Integer(required=False)

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
