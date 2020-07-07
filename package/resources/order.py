from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.order import OrderModel, OrderReceiverModel
from models.cart import CartModel
from models.users import UserSessionModel

from schema.order import OrderSchema, OrderReceiverSchema

from utils.strings_helper import gettext

order_schema = OrderSchema()
order_receiver_schema = OrderReceiverSchema()


class Order(Resource):
    @jwt_required
    def get(self, order_id):
        item = OrderModel.get_item(id=order_id)
        if not item:
            return {"message": gettext("order_not_found")}, 409
        return order_schema.dump(item), 200

    @jwt_required
    def delete(self, order_id):
        order = OrderModel.get_item(id=order_id)
        if not order.get("id"):
            return {"message": gettext("order_not_found")}, 409
        order.deactivate()
        order.save_to_db()
        return {"message": gettext("order_cancelled")}, 201


class Orders(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        orders = OrderModel.get_items()
        return {"orders": [order_schema.dump(order) for order in orders]}, 200


class OrderCreate(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        user = get_jwt_identity()
        req_data = request.get_json()
        client_ip = request.remote_addr
        session = UserSessionModel.get_item(user_id=user, ip=client_ip)
        cart = CartModel.get_item(user_id=user, session=session)
        if not cart:
            return {"message": gettext("no_item_in_cart")}
        req_data.update({"cart_id": cart.id})
        order = order_schema.load(
            req_data, instance=OrderModel.get_item(cart_id=cart.id)
        )
        if order.get("id"):
            return {"message": gettext("order_already_placed")}, 409
        print(order.get_json_data())
        order.save_to_db()
        print(order.get_json_data())
        return (
            {"message": gettext("order_placed"), "data": order_schema.dump(order)},
            201,
        )


class OrderReceiver(Resource):
    @jwt_required
    def get(self, id):
        order_receiver = OrderReceiverModel.get_item(id=id)
        if not order_receiver.get("id"):
            return {"message": "Order Receiver not found"}, 409
        return order_receiver_schema.dump(order_receiver), 200

    @jwt_required
    def put(self, id):
        user = get_jwt_identity()
        req_data = request.get_json()
        order_receiver = order_receiver_schema.load(
            req_data, instance=OrderReceiverModel.get_item(id=id), partial=True
        )
        if not order_receiver.get("id"):
            return {"message": gettext("order_receiver_not_found")}, 200
        if req_data.get("user") == "self":
            order_receiver.first_name = user.first_name
            order_receiver.last_name = user.last_name
            order_receiver.phone_no = user.phone_no
        order_receiver.save_to_db()
        return (
            {
                "message": gettext("order_receiver_updated"),
                "data": order_receiver_schema.dump(order_receiver),
            },
            201,
        )

    @jwt_required
    def delete(self, id):
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
        user = get_jwt_identity()
        req_data = request.get_json()
        order = OrderModel.get_item(id=req_data.get("order_id"))
        order_receiver = order_receiver_schema.load(
            req_data, instance=OrderReceiverModel.get_item(order=order)
        )
        if order_receiver.id:
            return {"message": gettext("order_receiver_already_settled")}, 200
        if req_data.get("user") == "self":
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
