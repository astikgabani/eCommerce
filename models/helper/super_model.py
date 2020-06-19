from typing import Dict, Any

import json

from flask import jsonify

from plugins.db import db

from enum import Enum


class SuperModel:
    @classmethod
    def get_active(cls, active=True):
        return cls.query.filter_by(active=active)

    @classmethod
    def get_query(cls, *args, **kwargs):
        query = cls.get_active(kwargs.get("active", True))
        for k, v in kwargs.items():
            query = query.filter(getattr(cls, k) == v)
        return query

    @classmethod
    def get_item(cls, *args, **kwargs):
        return cls.get_query(*args, **kwargs).first()

    @classmethod
    def get_items(cls, *args, **kwargs):
        return cls.get_query(*args, **kwargs).all()

    @classmethod
    def get_all(cls, active=True):
        return cls.get_active(active=active).all()

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def save_to_db(self, *args, **kwargs):
        self.pre_save()
        db.session.add(self)
        db.session.commit()
        self.post_save()

    def pre_delete(self):
        pass

    def post_delete(self):
        pass

    def delete_from_db(self, *args, **kwargs):
        self.pre_delete()
        db.session.delete(self)
        db.session.commit()
        self.post_delete()

    def get_json_data(self) -> Dict[str, Any]:
        data_dict = {}
        for attr in dir(self):
            # print(getattr(self, attr))
            if (
                not callable(getattr(self, attr))
                and not attr.startswith("__")
                and not attr.startswith("_")
            ):
                if attr not in ["metadata", "query"]:
                    value = getattr(self, attr)
                    if isinstance(value, Enum):
                        data_dict[attr] = value.value
                    if isinstance(value, list):
                        data_dict[attr] = [str(item) for item in value]
                    else:
                        data_dict[attr] = str(value)

        return json.loads(jsonify(data_dict).response[0].decode())

    def get(self, attr):
        if (
            not callable(getattr(self, attr))
            and not attr.startswith("__")
            and not attr.startswith("_")
            and attr not in ["metadata", "query"]
        ):
            value = getattr(self, attr)
            if isinstance(value, list):
                return [opt if opt.active else None for opt in value]
            elif isinstance(value, Enum):
                return value.value
            else:
                return value
        return None

    def set(self, attr, attr_value):
        if (
            not callable(getattr(self, attr))
            and not attr.startswith("__")
            and not attr.startswith("_")
            and attr not in ["metadata", "query"]
        ):
            value = getattr(self, attr)
            if isinstance(value, list):
                return setattr(self, attr, value.append(attr_value))
            elif isinstance(value, Enum):
                return setattr(self, attr, attr_value)
            else:
                return setattr(self, attr, attr_value)
        return None

    def deactivate(self):
        setattr(self, "active", False)
        return getattr(self, "active")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
