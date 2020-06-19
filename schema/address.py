from marshmallow import RAISE, INCLUDE, pre_load
from marshmallow_enum import EnumField

from plugins.ma import ma

from models.address import AddressModel, AddressTypeEnum
from models.helper.enums import CountryEnum


class AddressSchema(ma.SQLAlchemyAutoSchema):
    type = EnumField(AddressTypeEnum, by_name=True)
    country = EnumField(CountryEnum, by_name=True)

    class Meta:
        model = AddressModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        dump_only = ("id",)
        exclude = ("created", "updated", "active")
        unknown = RAISE
        load_instance = True


class AddressSchemaWithId(ma.SQLAlchemyAutoSchema):
    type = EnumField(AddressTypeEnum, by_name=True)
    country = EnumField(CountryEnum, by_name=True)

    class Meta:
        model = AddressModel
        datetimeformat = "%Y-%m-%dT%H:%M:%S"
        include_fk = True
        exclude = ("created", "updated", "active")
        unknown = INCLUDE
        load_instance = True

    @pre_load
    def slugify_name(self, in_data, **kwargs):
        in_data["address_id"] = in_data.get("id", None)
        in_data.pop("id", None)
        return in_data
