from models.helper.super_model import SuperModel, db

from datetime import datetime


class ReviewModel(db.Model, SuperModel):
    __tablename__ = "review"

    # there would be "product" and "user" columns
    # user
    # product
    id = db.Column(db.Integer, primary_key=True)
    ratings = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def pre_save(self):
        assert 0 > self.ratings >= 5, "ratings should be between 1 and 5"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.ratings}>"
