from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_optional,
    get_current_user,
)

from models.cart import CartModel, CartItemsModel
from models.coupons import CouponModel
from models.products import ProductModel
from models.users import UserSessionModel

from schema.cart import CartSchema, CartItemSchema
from schema.users import UserSessionSchema

from utils.strings_helper import gettext

cart_schema = CartSchema()
cart_item_schema = CartItemSchema()

user_session_schema = UserSessionSchema()


class Cart(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        if not cart:
            return {"message": gettext("cart_not_found")}, 409
        return cart_schema.dump(cart), 200

    @classmethod
    @jwt_optional
    def post(cls):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(user_id=user, ip=client_ip)
        if not session:
            session_info = {"ip": client_ip}
            session = user_session_schema.load(session_info)
            session.save_to_db()
        cart_data = {"session_id": session.id}
        cart = cart_schema.load(
            cart_data, instance=CartModel.get_item(session_id=session.id)
        )
        if cart.id:
            return {"message": gettext("cart_already_created")}, 409
        if user:
            cart.user_id = user
        cart.save_to_db()
        return (
            {"message": gettext("cart_created"), "data": cart_schema.dump(cart)},
            201,
        )

    @classmethod
    @jwt_optional
    def delete(cls):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_item(user_id=user, session=session)
        if not cart:
            return {"message": gettext("cart_not_found")}, 409
        cart.deactivate()
        cart.save_to_db()
        return (
            {"message": gettext("cart_deleted")},
            200,
        )


class CartItem(Resource):
    @classmethod
    @jwt_optional
    def get(cls):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        return (
            {
                "cart_items": [
                    cart_item_schema.dump(cart_item)
                    for cart_item in cart.get("cart_items")
                ]
            },
            200,
        )

    @classmethod
    @jwt_optional
    def post(cls):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        req_data = request.get_json()
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session=session)
        product = ProductModel.get_item(id=req_data.get("product_id"))
        if not product:
            return {"message": gettext("product_not_found")}, 409
        cart_item = cart_item_schema.load(req_data, instance=CartItemsModel.get_item(product_id=product.id, attr_option_id=req_data.get("attr_option_id")))
        if cart_item.id:
            cart_item.quantity += 1
        cart_item.cart = cart
        cart_item.product = product
        cart_item.save_to_db()
        return (
            {
                "message": gettext("cart_item_added"),
                "data": cart_item_schema.dump(cart_item),
            },
            201,
        )

    @classmethod
    @jwt_optional
    def put(cls):
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session=session)
        cart_item = cart_item_schema.load(
            req_data,
            instance=CartItemsModel.get_item(
                cart=cart, product_id=req_data.get("product_id")
            ),
        )
        if not cart_item.id:
            return {"message": gettext("cart_item_not_found")}, 409
        cart_item.save_to_db()
        return (
            {
                "message": gettext("cart_item_updated"),
                "data": cart_item_schema.dump(cart_item),
            },
            200,
        )

    @classmethod
    @jwt_optional
    def delete(cls):
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        cart_item = CartItemsModel.get_item(
            cart=cart, product_id=req_data.get("product_id")
        )
        if not cart_item:
            return {"message": gettext("cart_item_not_found")}, 409
        cart_item.deactivate()
        cart_item.save_to_db()
        return {"message": gettext("cart_item_deleted")}, 200


class ApplyCoupon(Resource):
    @jwt_optional
    def post(self, coupon_code):
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        coupon = CouponModel.get_item(code=coupon_code)
        cart.coupon = coupon
        cart.save_to_db()
        return (
            {"message": gettext("cart_coupon_apply"), "data": cart_schema.dump(cart)},
            200,
        )


class MergeTwoCart(Resource):
    @jwt_required
    def post(self, cart_id):
        user = get_current_user()
        user_cart = CartModel.get_or_create(user_id=user)
        cart = CartModel.get_item(id=cart_id)
        if not cart:
            return {"message": gettext("cart_not_found")}
        for item in cart.cart_items:
            item.cart = user_cart
        user_cart.save_to_db()
        cart.deactivate()
        cart.save_to_db()
        return (
            {"message": gettext("cart_merged"), "data": cart_schema.dump(user_cart)},
            200,
        )
