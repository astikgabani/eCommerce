from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
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
    @jwt_required(optional=True)
    def get(cls):
        """
        Return the cart object data.
        1. Get the session data from DB.
        2. load or create the cart obj from DB.
        3. Return the cart obj

        @return: Cart object
        @rtype: dict of cart obj details
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        return {"data": cart_schema.dump(cart)}, 200

    @classmethod
    @jwt_required(optional=True)
    def post(cls):
        """
        Return the cart object data.
        2. load or create the session obj from DB.
        3. load or create the cart obj from DB
        4. return the cart obj

        @return: Cart object
        @rtype: dict of cart obj details
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(user_id=user, ip=client_ip)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        return (
            {"message": gettext("cart_created"), "data": cart_schema.dump(cart)},
            201,
        )

    @classmethod
    @jwt_required(optional=True)
    def delete(cls):
        """
        Delete the cart.
        2. load or create the session obj from DB.
        3. load or create the cart obj from DB
        4. return the cart obj

        @return: message
        @rtype: dict of proper deleted msg
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_item(user_id=user, session=session)
        if not cart:
            return {"message": gettext("cart_not_found")}, 404
        cart.deactivate()
        cart.save_to_db()
        return (
            {"message": gettext("cart_deleted")},
            200,
        )


class CartItem(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        """
        Get the cart items.
        1. load or create the session obj from DB.
        2. load or create the cart obj from DB
        3. return the list of cart-items of the cart.

        @return: List of the items of cart
        @rtype: dict of list containing the items
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        return (
            {
                "data": [
                    cart_item_schema.dump(cart_item)
                    for cart_item in cart.get("cart_items")
                ]
            },
            200,
        )

    @classmethod
    @jwt_required(optional=True)
    def post(cls):
        """
        Add the items to cart.
        1. load or create the session obj from DB.
        2. load or create the cart obj from DB
        3. get the product from the DB.
        4. if product not found in DB, return the 409 conflict
        5. read the quantity and remove it from request data
        6. load the cart_item and if any cart_item found to be in cart, increase the quantity.
        7. if any cart_item not found to be in cart, add that product.
        8. save to DB and return the added cart item.

        @return: added cart_item
        @rtype: dict of newly added item
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        req_data = request.get_json()
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session=session)
        product = ProductModel.get_item(id=req_data.get("product_id"))
        if not product:
            return {"message": gettext("product_not_found")}, 404
        quantity = req_data.pop("quantity", 0)
        cart_item = cart_item_schema.load(
            req_data,
            instance=CartItemsModel.get_item(
                cart_id=cart.id,
                product_id=product.id,
                attr_option_id=req_data.get("attr_option_id"),
            ),
        )
        if cart_item.id:
            cart_item.quantity += int(quantity) or 1
        else:
            cart_item.quantity = int(quantity)
            cart_item.cart = cart
            cart_item.product = product
        cart_item.save_to_db()
        return (
            {
                "message": gettext("cart_item_added"),
                "data": cart_item_schema.dump(cart_item),
            },
            200,
        )

    @classmethod
    @jwt_required(optional=True)
    def put(cls):
        """
        Add the items to cart.
        1. load or create the session obj from DB.
        2. load or create the cart obj from DB
        3. load the cart_item and if any cart_item not found to be in cart, return 409 conflict.
        4. save to DB and return the updated cart item.

        @todo: Need to handle the scenario when user hit the api with the quantity 0 (Delete the cart_item)

        @return: added cart_item
        @rtype: dict of newly added item
        """
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session=session)
        cart_item = cart_item_schema.load(
            req_data,
            instance=CartItemsModel.get_item(
                cart=cart,
                product_id=req_data.get("product_id"),
                attr_option_id=req_data.get("attr_option_id"),
            ),
        )
        if not cart_item.id:
            return {"message": gettext("cart_item_not_found")}, 404
        cart_item.save_to_db()
        return (
            {
                "message": gettext("cart_item_updated"),
                "data": cart_item_schema.dump(cart_item),
            },
            200,
        )

    @classmethod
    @jwt_required(optional=True)
    def delete(cls):
        """
        remove the item from the cart.
        1. load or create the session obj from DB.
        2. load or create the cart obj from DB
        3. load the cart_item and if any cart_item found to be in cart.
        4. if any cart_item not found to be in cart, return 409 conflict.
        5. deactivate the cart_item
        6. save to DB and return the delete msg.

        @return: delete msg
        @rtype: dict of string
        """
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        cart_item = CartItemsModel.get_item(
            cart=cart,
            product_id=req_data.get("product_id"),
            attr_option_id=req_data.get("attr_option_id"),
        )
        if not cart_item:
            return {"message": gettext("cart_item_not_found")}, 404
        cart_item.delete_from_db()
        return {"message": gettext("cart_item_deleted")}, 200


class ApplyCoupon(Resource):
    @jwt_required()
    def post(self, coupon_code):
        """
        Apply the coupon on the cart.
        1. load or create the session obj from DB.
        2. load or create the cart obj from DB
        3. load the coupon from the db.
        4. if coupon not found, return the not found error
        5. assign the coupon
        6. save to DB and return the cart data.

        @return: updated cart
        @rtype: dict of cart data
        """
        coupon = CouponModel.get_item(code=coupon_code)
        if not coupon:
            return {"message": gettext("coupon_not_found")}, 404
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        if not cart.cart_items:
            return {"message": gettext("cart_should_not_be_empty")}, 400
        cart.coupon = coupon
        cart.save_to_db()
        return (
            {"message": gettext("cart_coupon_apply"), "data": cart_schema.dump(cart)},
            200,
        )


class MergeTwoCart(Resource):
    @jwt_required()
    def post(self, cart_id):
        """
        @param: cart_id
        @type: int

        Merge the cart with user and cart without user.
        1. load or create the user's cart obj from DB
        2. load or create the another cart obj from DB
        3. if another cart not found, return 404 not found
        4. loop over the cart items and change the cart value
        5. deactivate the another cart
        6. save to DB and return the cart data.

        @todo: Need to handle the scenario, which is - same product present in both the cart.

        @return: updated cart
        @rtype: dict of cart data
        """
        user = get_jwt_identity()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(ip=client_ip, user_id=user)
        user_cart = CartModel.get_or_create(user_id=user, session_id=session.id)
        cart = CartModel.get_item(id=cart_id)
        if not cart:
            return {"message": gettext("cart_not_found")}, 404
        for item in cart.cart_items:
            item.cart = user_cart
        user_cart.save_to_db()
        cart.deactivate()
        cart.save_to_db()
        return (
            {"message": gettext("cart_merged"), "data": cart_schema.dump(user_cart)},
            200,
        )
