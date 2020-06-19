from typing import Any, Optional, Mapping

from marshmallow import fields, RAISE
from plugins.ma import ma

from models.products import (
    ProductModel,
    ProductAttributeModel,
    ProductAttributeOptionsModel,
    ProductImageModel,
)

from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {"Invalid": "Not a valid image"}

    def _deserialize(
        self,
        value: Any,
        attr: Optional[str],
        data: Optional[Mapping[str, Any]],
        **kwargs
    ):
        if not value:
            return None

        if not isinstance(value, FileStorage):
            self.fail("Invalid")  # Raise ValidationError

        return value


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        include_fk = True
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class ProductAttributeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductAttributeModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class ProductAttributeOptionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductAttributeOptionsModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class ProductImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductImageModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class ImageSchema(ma.Schema):
    image = FileStorageField(required=True)


class ProductAttributeAllSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductAttributeModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = False
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True

    attrs_options = ma.List(ma.Nested(ProductAttributeOptionsSchema))


class ProductAllSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        include_fk = False
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True

    attrs = ma.List(ma.Nested(ProductAttributeAllSchema))
