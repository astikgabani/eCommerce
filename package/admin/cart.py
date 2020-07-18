from admin.helper.helper import SuperView

from models.cart import CartModel, CartItemsModel
from models.order import OrderModel


class CartView(SuperView):

    inline_models = [CartItemsModel, OrderModel]

    def __init__(self, model=CartModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class CartItemView(SuperView):
    def __init__(self, model=CartItemsModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
