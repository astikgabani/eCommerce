from marshmallow import RAISE
from marshmallow_enum import EnumField

from plugins.ma import ma

from models.coupons import CouponModel
from models.helper.enums import CouponTypeEnum


class CouponSchema(ma.SQLAlchemyAutoSchema):
    type = EnumField(CouponTypeEnum, by_name=True)

    class Meta:
        model = CouponModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id", "code")
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True
