from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.address import AddressModel

from schema.address import AddressSchema, AddressSchemaWithId

from utils.strings_helper import gettext

address_schema = AddressSchema()
address_schema_with_id = AddressSchemaWithId()


class Address(Resource):
    @jwt_required()
    def get(self):
        """
        Getting the list of address of specific user(user detect using it's access-token).
        @return: List of addresses of the access-token of the user.
        @rtype: {"addresses" : [<Dict of address-1>, <Dict of address-2>]}
        """
        user = get_jwt_identity()
        addresses = AddressModel.get_items(user_id=user)
        return (
            {"addresses": [address_schema.dump(address) for address in addresses]},
            200,
        )

    @jwt_required()
    def post(self):
        """
        Create the new address as per the request data.
        1. Load the data with the help of schema validation.
        2. If address is already created, return conflict error message.
        3. Assign the user which we get from the access-token.
        4. Save to DB and return 200 response.

        @return: Newly created address data after dumping it with schema.
        @rtype: {"data": <Dict-of-created-address>} along with proper msg
        """
        current_user = get_jwt_identity()
        req_data = request.get_json()
        address = address_schema.load(req_data)
        address.user_id = current_user
        address.save_to_db()
        return (
            {
                "message": gettext("address_created"),
                "data": address_schema.dump(address),
            },
            200,
        )

    @jwt_required()
    def put(self):
        """
        Update the already created address as per the request data.
        1. Load the data with the help of schema validation.
        2. If address is not created, return 404 Not Found.
        3. Save to DB and return 200 response.

        @return: Updated address data after dumping it with schema.
        @rtype: {"data": <Dict-of-created-address>} along with proper msg
        """
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
                "message": gettext("address_updated"),
                "data": address_schema.dump(address),
            },
            200,
        )

    @jwt_required()
    def delete(self):
        """
        Delete the address as per the request data.
        1. Get the item from DB with the user(from access-token) and id(Request data).
        2. If address is not found in DB, return 404 Not Found.
        3. Deactivate the Address in db and Save to DB and return 200 response.

        @return: Updated address data after dumping it with schema.
        @rtype: dict along with proper msg
        """
        user = get_jwt_identity()
        req_data = request.get_json()
        address = AddressModel.get_item(id=req_data.get("id"), user_id=user)
        if not address:
            return {"message": gettext("address_not_found")}, 404
        address.deactivate()
        address.save_to_db()
        return (
            {"message": gettext("address_deleted")},
            200,
        )
