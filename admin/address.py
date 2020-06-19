from admin.helper.helper import SuperView

from models.address import AddressModel


class AddressView(SuperView):

    inline_models = []

    def __init__(self, model=AddressModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
