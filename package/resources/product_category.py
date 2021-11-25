from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.product_category import ProductCategoryModel

from schema.product_category import ProductCategorySchema

from utils.strings_helper import gettext
from utils.user_roles import required_role

product_category_schema = ProductCategorySchema()


class ProductCategory(Resource):
    def get(self, id):
        """
        @param id: product category id
        @type id: int

        Get the detail of specific category
        1. fetch the product category based on id from db
        2. if item not found, return 404 not found
        3. return the product category details.

        @return: product category details
        @rtype: dict of product category details
        """
        item = ProductCategoryModel.get_item(id=id)
        if not item:
            return {"message": gettext("product_category_not_found")}, 409
        return {"data": product_category_schema.dump(item)}, 200

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def put(self, id):
        """
        @param id: product category id
        @type id: int

        Update the detail of specific category
        1. load the product category from db along with the request data
        2. if category not found, return 404 not found
        3. save to db and return the updated product category details.

        @return: updated product category details
        @rtype: dict of product category details
        """
        req_data = request.get_json()
        category = product_category_schema.load(
            req_data, instance=ProductCategoryModel.get_item(id=id), partial=True
        )
        if not category:
            return {"message": gettext("product_category_not_found")}, 404
        category.save_to_db()
        return (
            {
                "message": gettext("product_category_updated"),
                "data": product_category_schema.dump(category),
            },
            201,
        )

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def delete(self, id):
        """
        @param id: product category id
        @type id: int

        Delete the detail of specific category
        1. fetch the product category from db based on id
        2. if category not found, return 404 not found
        3. deactivate, save to db and return the proper delete msg.

        @return: delete msg
        @rtype: dict of deletion msg
        """
        category = ProductCategoryModel.get_item(id=id)
        if not category:
            return {"message": gettext("product_category_not_found")}, 404
        category.deactivate()
        category.save_to_db()
        return {"message": gettext("product_category_deleted")}, 201


class ProductCategoryCreate(Resource):
    def get(self, parent_id):
        """
        @param parent_id: Parent id of specified category
        @type parent_id: int

        Return the list of sub categories of specified category
        1. fetch the all items which have specified parent id.
        2. return the list of all details of sub category.

        @return: return the list of all details of sub category.
        @rtype: dict of list
        """
        items = ProductCategoryModel.get_items(parent_id=parent_id)
        return {"data": [product_category_schema.dump(item) for item in items]}

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self, parent_id):
        """
        @param parent_id: Parent id of specified category
        @type parent_id: int

        crete a category under some parent category
        1. load the all items from db along with request data.
        2. if category id found, return 409 conflict
        3. assign the parent id to new category.
        4. save to db and return newly created category details.

        @return: return the list of all details of sub category.
        @rtype: dict of list
        """
        req_data = request.get_json()
        category = product_category_schema.load(
            req_data,
            instance=ProductCategoryModel.get_item(
                name=req_data.get("name"), parent_id=parent_id
            ),
        )
        if category.id:
            return {"message": gettext("product_category_already_created")}, 409
        category.parent_id = parent_id
        category.save_to_db()
        return (
            {
                "message": gettext("product_category_created"),
                "data": product_category_schema.dump(category),
            },
            201,
        )
