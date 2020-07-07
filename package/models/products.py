from models.helper.super_model import SuperModel, db
from models.helper.utils import unique_slug_generator

from datetime import datetime

coupons_table = db.Table(
    "coupons_table",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("coupon_id", db.Integer, db.ForeignKey("coupon.id")),
)

image_table = db.Table(
    "image_table",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
    db.Column("image_id", db.Integer, db.ForeignKey("product_image.id")),
)


class ProductModel(db.Model, SuperModel):
    __tablename__ = "product"

    # category
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=True
    )

    attrs = db.relationship("ProductAttributeModel", backref="product", lazy=True)
    coupons = db.relationship(
        "CouponModel",
        secondary=coupons_table,
        backref=db.backref("products", lazy="select"),
    )
    cart_item = db.relationship("CartItemsModel", backref="product", lazy=True)
    images = db.relationship("ProductImageModel", backref="product", lazy=True)
    reviews = db.relationship("ReviewModel", backref="product", lazy=False)

    def __repr__(self) -> str:
        return f"<ProductModel {self.name}>"

    def pre_save(self):
        self.slug = self.slug if self.slug else unique_slug_generator(self)
        assert self.price > 0, "Price can't be zero"


class ProductAttributeModel(db.Model, SuperModel):
    __tablename__ = "product_attr"

    # Here we will have a column name "product" which is the object of product
    # product
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=True)

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    attrs_options = db.relationship(
        "ProductAttributeOptionsModel", backref="attr", lazy=True,
    )


class ProductAttributeOptionsModel(db.Model, SuperModel):
    __tablename__ = "product_attr_option"

    # Here we will have a column name "attr" which have object of product attribute
    # attr
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=True)
    price_change = db.Column(db.Float(precision=2), default=0.00)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attr_id = db.Column(db.Integer, db.ForeignKey("product_attr.id"), nullable=True)

    cart_items = db.relationship("CartItemsModel", backref="product_option", lazy=True)

    def pre_save(self):
        assert self.price_change >= 0, "Price change can't be negetive"


class ProductImageModel(db.Model, SuperModel):
    __tablename__ = "product_image"

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product_slug = db.Column(
        db.String(80), db.ForeignKey("product.slug"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.image_name}>"
