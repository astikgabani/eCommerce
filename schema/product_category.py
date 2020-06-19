from marshmallow import RAISE

from plugins.ma import ma

from models.product_category import ProductCategoryModel


class ProductCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductCategoryModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True
