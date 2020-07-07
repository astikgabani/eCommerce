from admin.helper.helper import SuperView

from models.coupons import CouponModel
from models.cart import CartModel


class CouponView(SuperView):

    inline_models = [CartModel]

    def __init__(self, model=CouponModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
