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
        item = ProductCategoryModel.get_item(id=id)
        if not item:
            return {"message": gettext("product_category_not_found")}, 409
        return product_category_schema.dump(item), 200

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def put(self, id):
        req_data = request.get_json()
        category = product_category_schema.load(
            req_data, instance=ProductCategoryModel.get_item(id=id), partial=True
        )
        if not category:
            return {"message": gettext("product_category_not_found")}, 409
        category.save_to_db()
        return (
            {
                "message": gettext("product_category_updated"),
                "data": product_category_schema.dump(category),
            },
            201,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def delete(self, id):
        category = ProductCategoryModel.get_item(id=id)
        if not category:
            return {"message": gettext("product_category_not_found")}, 409
        category.deactivate()
        category.save_to_db()
        return {"message": gettext("product_category_deleted")}, 201


class ProductCategoryCreate(Resource):
    def get(self, parent_id):
        items = ProductCategoryModel.get_items(parent_id=parent_id)
        return {"data": [product_category_schema.dump(item) for item in items]}

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self, parent_id):
        req_data = request.get_json()
        item = ProductCategoryModel.get_item(
            name=req_data.get("name"), parent_id=parent_id
        )
        category = product_category_schema.load(req_data, instance=item)
        if category.get("id"):
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
