from marshmallow import RAISE

from plugins.ma import ma

from models.review import ReviewModel


class ProductReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id", "product_id", "user_id")
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True
