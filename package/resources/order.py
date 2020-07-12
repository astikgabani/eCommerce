"""
@todo: There could be a security bug,
if some user has an access-token and
if he trying to access the order receiver details using some dummy id, he might be able to get it.
so it's information leakage
"""

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.order import OrderModel, OrderReceiverModel
from models.cart import CartModel
from models.users import UserSessionModel, UserModel

from schema.order import OrderSchema, OrderReceiverSchema

from utils.strings_helper import gettext

order_schema = OrderSchema()
order_receiver_schema = OrderReceiverSchema()


class Order(Resource):
    @jwt_required
    def get(self, order_id):
        """
        @param order_id: id of the order
        @type order_id: int

        Get the detail os order by the user.
        1. get the order from db
        2. if no order found, return 404 not found
        3. return the order data

        @return: detail of specific order
        @rtype: dict of order details
        """
        user = get_jwt_identity()
        item = OrderModel.get_item(id=order_id, user_id=user)
        if not item:
            return {"message": gettext("order_not_found")}, 404
        return {"data": order_schema.dump(item)}, 200

    @jwt_required
    def delete(self, order_id):
        """
        @param order_id: id of the order
        @type order_id: int

        Cancel the order.
        1. get the order from db
        2. if no order found, return 404 not found
        3. deactivate the order, save to db and return the cancelled msg

        @return: detail of specific order
        @rtype: dict of order details
        """
        user = get_jwt_identity()
        order = OrderModel.get_item(id=order_id, user_id=user)
        if not order.get("id"):
            return {"message": gettext("order_not_found")}, 404
        order.deactivate()
        order.save_to_db()
        return {"message": gettext("order_cancelled")}, 201


class Orders(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        """
        Get the list of all orders
        1. get the all order of specific user
        2. return the list of all orders

        @return: list of all orders placed by specific user
        @rtype: dict of list
        """
        user = get_jwt_identity()
        orders = OrderModel.get_items(user_id=user)
        return {"orders": [order_schema.dump(order) for order in orders]}, 200


class OrderCreate(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """
        Placed an order.
        1. load or create a session
        2. fetch the cart from db
        3. check for empty cart. return if found empty
        4. load the request data.
        5. if order found already placed, return that err msg
        6. save to db and return the order details

        @return: details of the placed order
        @rtype: dict of order's detail
        """
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_or_create(user_id=user, ip=client_ip)
        cart = CartModel.get_item(user_id=user, session=session)
        if not cart and not cart.cart_items:
            return {"message": gettext("no_item_in_cart")}
        req_data.update({"cart_id": cart.id})
        order = order_schema.load(
            req_data, instance=OrderModel.get_item(cart_id=cart.id)
        )
        if order.get("id"):
            return {"message": gettext("order_already_placed")}, 409
        order.save_to_db()
        return (
            {"message": gettext("order_placed"), "data": order_schema.dump(order)},
            201,
        )


class OrderReceiver(Resource):
    @jwt_required
    def get(self, id):
        """
        @param id: id of order receiver
        @type id: int

        Get the order receiver details.
        1. fetch the details of order receiver from db
        2. if not found, return that
        3. return the order receiver details

        @return: order receiver details
        @rtype: dict of details
        """
        order_receiver = OrderReceiverModel.get_item(id=id)
        if not order_receiver.get("id"):
            return {"message": "Order Receiver not found"}, 404
        return {"data": order_receiver_schema.dump(order_receiver)}, 200

    @jwt_required
    def put(self, id):
        """
        @param id: id of order receiver
        @type id: int

        Update order receiver details.
        1. load the order receiver request data
        2. if not found, return that msg
        3. if value of user is 'self', update the details user it self
        4. save to db and return updated details of order receiver

        @return: updated order receiver details
        @rtype: dict of details
        """
        user_id = get_jwt_identity()
        req_data = request.get_json()
        order_receiver = order_receiver_schema.load(
            req_data, instance=OrderReceiverModel.get_item(id=id), partial=True
        )
        if not order_receiver.get("id"):
            return {"message": gettext("order_receiver_not_found")}, 404
        if req_data.get("user") == "self":
            user = UserModel.get_item(id=user_id)
            order_receiver.first_name = user.first_name
            order_receiver.last_name = user.last_name
            order_receiver.phone_no = user.phone_no
        order_receiver.save_to_db()
        return (
            {
                "message": gettext("order_receiver_updated"),
                "data": order_receiver_schema.dump(order_receiver),
            },
            200,
        )

    @jwt_required
    def delete(self, id):
        """
        @param id: id of order receiver
        @type id: int

        deactivate order receiver details.
        1. fetch the order receiver details from db
        2. if not found, return 404 not found
        3. deactivate, save to db and return updated details of order receiver

        @return: updated order receiver details
        @rtype: dict of details
        """
        order_receiver = OrderReceiverModel.get_item(id=id)
        if not order_receiver:
            return {"message": gettext("order_receiver_not_found")}, 409
        order_receiver.deactivate()
        order_receiver.save_to_db()
        return {"message": gettext("order_receiver_deleted")}, 200


class OrderReceiverCreate(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """
        Creating a new order receiver.
        1. fetch the order receiver details.
        2. load the order receiver details from request data
        3. if order receiver already settled, return 409 conflict
        4. if user is 'self', assign user itself as order receiver
        5. save to db and return the created details.

        @return: Newly created order receiver details.
        @rtype: dict of newly created order receiver details.
        """
        user_id = get_jwt_identity()
        req_data = request.get_json()
        order = OrderModel.get_item(id=req_data.get("order_id"))
        order_receiver = order_receiver_schema.load(
            req_data, instance=OrderReceiverModel.get_item(order=order)
        )
        if order_receiver.id:
            return {"message": gettext("order_receiver_already_settled")}, 409
        if req_data.get("user") == "self":
            user = UserModel.get_item(id=user_id)
            order_receiver.first_name = user.first_name
            order_receiver.last_name = user.last_name
            order_receiver.phone_no = user.phone_no
        order_receiver.save_to_db()
        return (
            {
                "message": gettext("order_receiver_created"),
                "data": order_receiver_schema.dump(order_receiver),
            },
            201,
        )
