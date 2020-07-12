from models.helper.super_model import SuperModel, db
from models.helper.enums import CouponTypeEnum

from datetime import datetime


class CouponModel(db.Model, SuperModel):
    __tablename__ = "coupon"

    # products
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(20), nullable=False)
    type = db.Column(db.Enum(CouponTypeEnum), default=CouponTypeEnum.percentage)
    value = db.Column(db.Integer, nullable=False)
    max_value = db.Column(db.Integer, nullable=True)
    start = db.Column(db.DateTime, nullable=False)
    expire = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart = db.relationship("CartModel", backref="coupon", lazy=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.code}>"

    def pre_save(self):
        assert (
            self.start < self.expire
        ), "Coupon's start date is greater than it's expiry date"

    def get_discount_price(self, cart_item_price):
        current_time = datetime.utcnow()
        if self.start < current_time < self.expire:
            if self.type == CouponTypeEnum.percentage:
                disc_price = (cart_item_price * self.value) / 100
                return min(disc_price, self.max_value, cart_item_price)
            else:
                return min(cart_item_price, self.value)
        return 0
