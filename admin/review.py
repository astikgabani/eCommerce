from admin.helper.helper import SuperView

from models.review import ReviewModel


class ReviewView(SuperView):

    inline_models = []

    def __init__(self, model=ReviewModel, *args, **kwargs):
        super().__init__(model=model, *args, **kwargs)
