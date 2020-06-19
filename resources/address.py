from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.address import AddressModel

from schema.address import AddressSchema, AddressSchemaWithId

from utils.strings_helper import gettext

address_schema = AddressSchema()
address_schema_with_id = AddressSchemaWithId()


class Address(Resource):
    @jwt_required
    def get(self):
        user = get_jwt_identity()
        addresses = AddressModel.get_items(user_id=user)
        return (
            {"addresses": [address_schema.dump(address) for address in addresses]},
            200,
        )

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        req_data = request.get_json()
        address = address_schema.load(req_data, partial=True)
        address.user_id = address.get("user_id") or current_user
        address.save_to_db()
        return (
            {
                "message": gettext("address_created"),
                "data": address_schema.dump(address),
            },
            200,
        )

    @jwt_required
    def put(self):
        user = get_jwt_identity()
        req_data = request.get_json()
        address = address_schema_with_id.load(
            req_data,
            instance=AddressModel.get_item(id=req_data.get("id"), user_id=user),
            partial=True,
        )
        if not address.id:
            return {"message": gettext("address_not_found")}, 404
        address.save_to_db()
        return (
            {
                "message": gettext("address_not_found"),
                "data": address_schema.dump(address),
            },
            200,
        )

    @jwt_required
    def delete(self):
        user = get_jwt_identity()
        req_data = request.get_json()
        item = AddressModel.get_item(id=req_data.get("id"), user_id=user)
        address = address_schema_with_id.load(req_data, instance=item, partial=True)
        if not address.id:
            return {"message": gettext("address_not_found")}, 404
        address.deactivate()
        address.save_to_db()
        return (
            {"message": gettext("address_deleted")},
            200,
        )
