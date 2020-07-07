from admin.helper.helper import SuperView

from models.products import (
    ProductModel,
    ProductImageModel,
    ProductAttributeModel,
    ProductAttributeOptionsModel,
)
from models.cart import CartItemsModel
from models.review import ReviewModel


class ProductView(SuperView):

    inline_models = [
        ProductAttributeModel,
        CartItemsModel,
        ProductImageModel,
        ReviewModel,
    ]

    def __init__(self, model=ProductModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class ProductImageView(SuperView):

    inline_models = []

    def __init__(self, model=ProductImageModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class ProductAttributeView(SuperView):

    inline_models = [ProductAttributeOptionsModel]

    def __init__(self, model=ProductAttributeModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)


class ProductAttributeOptionsView(SuperView):

    inline_models = []

    def __init__(self, model=ProductAttributeOptionsModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
