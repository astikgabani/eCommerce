from models.helper.super_model import SuperModel, db
from models.helper.enums import AddressTypeEnum, CountryEnum

from datetime import datetime


class AddressModel(db.Model, SuperModel):
    __tablename__ = "address"

    # user
    # orders
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(AddressTypeEnum), default=AddressTypeEnum.shipping)
    address_line_1 = db.Column(db.String(200), nullable=False)
    address_line_2 = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.Enum(CountryEnum), default=CountryEnum.india)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.type.value}>"
