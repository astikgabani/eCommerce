from admin.helper.helper import SuperView

from models.order import OrderModel, OrderReceiverModel
from models.address import AddressModel


class OrderView(SuperView):

    inline_models = [AddressModel]

    def __init__(self, model=OrderModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class OrderReceiverView(SuperView):

    inline_models = [OrderModel]

    def __init__(self, model=OrderReceiverModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
