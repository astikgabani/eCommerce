from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.coupons import CouponModel
from models.products import ProductModel

from schema.coupons import CouponSchema

from utils.strings_helper import gettext
from utils.user_roles import required_role

coupon_schema = CouponSchema()


class Coupon(Resource):
    def get(self, code):
        """
        @param code: Actual coupon code
        @type code: string

        Get the details of coupons.
        1. get the details of coupon from DB.
        2. if coupon not found, return 404 not found
        3. else return the coupon data

        @return: List of specific coupon
        @rtype: dict containing data of coupon
        """
        item = CouponModel.get_item(code=code)
        if not item:
            return {"message": gettext("coupon_not_found")}, 404
        return {"data": coupon_schema.dump(item)}, 200

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self, code):
        """
        @param code: Actual coupon code
        @type code: string

        create a coupon.
        1. load the request data.
        2. if coupon found, return 409 conflict
        3. save to DB and return the newly created coupon data.

        @return: Newly created coupon data
        @rtype: dict containing newly created data of coupon
        """
        req_data = request.get_json()
        coupon = coupon_schema.load(req_data, instance=CouponModel.get_item(code=code))
        if coupon.id:
            return {"message": "Coupon is already present"}, 409
        coupon.code = code
        coupon.save_to_db()
        return (
            {
                "message": gettext("coupon_already_created"),
                "data": coupon_schema.dump(coupon),
            },
            201,
        )

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def put(self, code):
        """
        @param code: Actual coupon code
        @type code: string

        create a coupon.
        1. load the request data.
        2. if coupon not found, return 404 not found
        3. save to DB and return the updated coupon data.

        @return: Updated coupon data
        @rtype: dict containing updated data of coupon
        """
        req_data = request.get_json()
        coupon = coupon_schema.load(
            req_data, instance=CouponModel.get_item(code=code), partial=True
        )
        if not coupon.id:
            return {"message": gettext("coupon_not_found")}, 404
        coupon.save_to_db()
        return (
            {"message": gettext("coupon_updated"), "data": coupon_schema.dump(coupon), },
            200,
        )

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def delete(self, code):
        """
        @param code: Actual coupon code
        @type code: string

        create a coupon.
        1. find the coupon.
        2. if coupon not found, return 404 not found
        3. deactivate and save to DB

        @return: delete msg
        @rtype: dict containing deleted message
        """
        coupon = CouponModel.get_item(code=code)
        if not coupon:
            return {"message": gettext("coupon_not_found")}, 404
        coupon.deactivate()
        coupon.save_to_db()
        return {"message": gettext("coupon_deleted")}, 200


class Coupons(Resource):
    @classmethod
    def get(cls):
        """
        @return: Get the list of all the coupon
        @rtype: dict of the list containing coupon data
        """
        coupons = CouponModel.get_items()
        return {"coupons": [coupon_schema.dump(coupon) for coupon in coupons]}, 200


class ProductCouponMapping(Resource):
    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self, code):
        """
        @param code: Coupon Code
        @type code: String

        Assign the coupon to the specified products.
        1. get the coupon from db
        2. loop over the product_ids of request data. and applied coupon on that products

        @return: coupon details
        @rtype: dict of coupon data
        """
        req_data = request.get_json()
        coupon = CouponModel.get_item(code=code)
        for product in req_data.get("product_ids"):
            item = (
                ProductModel.get_item(id=product)
                if not req_data.get("type") == "slug"
                else ProductModel.get_item(slug=product)
            )
            if item:
                coupon.products.append(item)
        return (
            {
                "message": gettext("coupon_product_mapping"),
                "data": coupon_schema.dump(coupon),
            },
            200,
        )
