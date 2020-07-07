from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

from plugins.db import db


class SuperView(ModelView):

    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    column_display_all_relations = False
    column_display_pk = True
    page_size = 20
    form_widget_args = {
        "created": {"readonly": True},
        "updated": {"readonly": True},
    }

    def on_model_change(self, form, model, is_created):
        model.pre_save()

    def after_model_change(self, form, model, is_created):
        print(dir(model))
        model.post_save()

    def __init__(self, model, *args, **kwargs):
        super().__init__(model=model, session=db.session, *args, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated
