from models.helper.super_model import SuperModel, db

from utils.strings_helper import gettext

from datetime import datetime


class CartModel(db.Model, SuperModel):
    __tablename__ = "cart"

    # there would be "cart_item" and "user" columns
    # user
    # session
    # coupon
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float(precision=2), default=0.00)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.ForeignKey("user.id"), nullable=True)
    session_id = db.Column(db.ForeignKey("user_session.id"), nullable=True)
    coupon_id = db.Column(db.ForeignKey("coupon.id"), nullable=True)

    cart_items = db.relationship("CartItemsModel", backref="cart", lazy=True)
    orders = db.relationship("OrderModel", backref="cart", lazy=True, uselist=False)

    @property
    def count_total(self):
        total_sum = 0
        if self.cart_items and isinstance(self.cart_items, list):
            for cart_item in self.cart_items:
                disc_price = 0
                cart_item_price = cart_item.get_price()
                if self.coupon in cart_item.product.coupons:
                    disc_price = self.coupon.get_discount_price(cart_item_price)
                total_sum += cart_item_price - disc_price
        return total_sum

    def pre_save(self):
        print(self.count_total)
        self.total = self.count_total
        assert self.total >= 0, "total is not valid"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

    @classmethod
    def get_or_create(cls, **kwargs):
        cart = cls.get_item(**kwargs)
        if cart:
            return cart
        new_cart = cls(**kwargs)
        new_cart.save_to_db()
        return new_cart


class CartItemsModel(db.Model, SuperModel):
    __tablename__ = "cart_items"

    # cart
    # cart_item
    # product
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart_id = db.Column(db.ForeignKey("cart.id"))
    product_id = db.Column(db.ForeignKey("product.id"))
    attr_option_id = db.Column(db.ForeignKey("product_attr_option.id"))

    def pre_save(self):
        if (
            self.product
            and len(self.product.attrs) > 0
        ):
            for attr in self.product.attrs:
                if len(attr.attrs_options) > 0:
                    assert (
                        self.attr_option_id is not None
                    ), "Attributes options should be choosen if attributes are present in product"
        assert self.quantity > 0, "Quantity is not valid"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.product_id}>"

    def get_price(self) -> float:
        price = self.product.price
        for attr in self.product.attrs:
            for option in attr.attrs_options:
                price += option.price_change
        return price

    def post_save(self):
        self.cart.total = self.cart.count_total
