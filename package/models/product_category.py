from models.helper.super_model import SuperModel, db

from datetime import datetime


class ProductCategoryModel(db.Model, SuperModel):
    __tablename__ = "product_category"

    # parent
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    value = db.Column(db.String(80), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey("product_category.id"), default=0)

    parent_rel = db.relationship(
        "ProductCategoryModel", remote_side=id, backref="parent", lazy=True
    )
    product = db.relationship("ProductModel", backref="category", lazy=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"
