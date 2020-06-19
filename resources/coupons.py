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
        item = CouponModel.get_item(code=code)
        if not item:
            return {"message": gettext("coupon_not_found")}, 409
        return {"data": coupon_schema.dump(item)}, 200

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self, code):
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

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def put(self, code):
        req_data = request.get_json()
        coupon = coupon_schema.load(
            req_data, instance=CouponModel.get_item(code=code), partial=True
        )
        if not coupon:
            return {"message": gettext("coupon_not_found")}, 409
        coupon.save_to_db()
        return (
            {"message": gettext("coupon_updated"), "data": coupon_schema.dump(coupon), },
            200,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def delete(self, code):
        coupon = CouponModel.get_item(code=code)
        if not coupon:
            return {"message": gettext("coupon_not_found")}, 409
        coupon.deactivate()
        coupon.save_to_db()
        return {"message": gettext("coupon_deleted")}, 200


class Coupons(Resource):
    @classmethod
    def get(cls):
        coupons = CouponModel.get_items()
        return {"coupons": [coupon_schema.dump(coupon) for coupon in coupons]}, 200


class ProductCouponMapping(Resource):
    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self, code):
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
                "data": coupon.get_json_data(),
            },
            200,
        )
