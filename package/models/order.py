from models.helper.super_model import SuperModel, db
from models.helper.enums import OrderStatusEnum, AddressTypeEnum

from datetime import datetime

import re


phone_regex = re.compile(r"[1-9][0-9]{9}")

order_address = db.Table(
    "order_address",
    db.Column("address_id", db.Integer, db.ForeignKey("address.id"), primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),
)


class OrderModel(db.Model, SuperModel):
    __tablename__ = "order"

    # order_receiver
    # cart
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(OrderStatusEnum), default=OrderStatusEnum.placed)
    shipping_cost = db.Column(db.Float(precision=2), default=0.00)
    total = db.Column(db.Float(precision=2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Addresses
    addresses = db.relationship(
        "AddressModel",
        secondary=order_address,
        lazy="subquery",
        backref=db.backref("orders", lazy=True),
    )

    order_receiver_id = db.Column(
        db.Integer, db.ForeignKey("order_receiver.id"), nullable=False
    )
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def deactivate(self):
        setattr(self, "status", OrderStatusEnum.cancelled)
        return getattr(self, "status")

    def pre_save(self):
        self.total = self.cart.count_total
        assert self.total > 0, "Order total can't be negative or Zero"
        assert (
            self.cart.user_id is not None
        ), "Only registered Users can placed the order"


class OrderReceiverModel(db.Model, SuperModel):
    __tablename__ = "order_receiver"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = db.relationship(
        "OrderModel", backref="order_receiver", lazy=False, uselist=False
    )

    def pre_save(self):
        assert phone_regex.match(str(self.phone_no)), "Phone No is not valid"
