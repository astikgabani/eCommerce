import os
import re
import stripe

from models.helper.super_model import SuperModel, db
from models.helper.enums import OrderStatusEnum, AddressTypeEnum, PaymentStatusEnum

from datetime import datetime



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
    # user
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(OrderStatusEnum), default=OrderStatusEnum.placed)
    shipping_cost = db.Column(db.Float(precision=2), default=0.00)
    payment_status = db.Column(db.Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    total = db.Column(db.Float(precision=2), default=0.00)
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

    order_receiver_id = db.Column(db.ForeignKey("order_receiver.id"), nullable=False)
    cart_id = db.Column(db.ForeignKey("cart.id"), nullable=False)
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    def deactivate(self):
        setattr(self, "status", OrderStatusEnum.cancelled)
        setattr(self, "active", False)
        return getattr(self, "status")

    def set_payment_status(self, status: str):
        self.payment_status = PaymentStatusEnum.__members__.get(status) or PaymentStatusEnum.pending
        self.save_to_db()

    def payment_amount(self):
        return int(self.total * 100)

    def payment_with_stripe(self, token: str) -> "stripe":
        stripe.api_key = os.getenv("STRIPE_API_KEY")

        return stripe.Charge.create(
            amount=self.payment_amount(),
            currency="inr",
            description="My First Test Charge (created for API docs)",
            source=token,
        )

    def post_save(self):
        # print(self.get_json_data())
        self.total = self.cart.count_total + self.shipping_cost
        assert self.total > 0, "Order total can't be negative or Zero"
        assert (
            self.cart.user_id is not None
        ), "Only registered Users can placed the order"

    def clear_all(self):
        self.cart.deactivate()


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
