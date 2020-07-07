from admin.helper.helper import SuperView

from models.product_category import ProductCategoryModel
from models.products import ProductModel


class ProductCategoryView(SuperView):

    inline_models = [ProductCategoryModel, ProductModel]

    def __init__(self, model=ProductCategoryModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
