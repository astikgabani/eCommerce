from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional

from models.review import ReviewModel

from schema.review import ProductReviewSchema

from utils.strings_helper import gettext

product_review_schema = ProductReviewSchema()


class ProductReview(Resource):
    @classmethod
    @jwt_optional
    def get(cls, product_id):
        user = get_jwt_identity()
        review = ReviewModel.get_item(product_id=product_id, user_id=user)
        return product_review_schema.dump(review), 200

    @classmethod
    @jwt_required
    def post(cls, product_id):
        user = get_jwt_identity()
        req_data = request.get_json()
        review = product_review_schema.load(
            req_data, instance=ReviewModel.get_item(user_id=user, product_id=product_id)
        )
        if review.get("id"):
            return (
                {"message": gettext("product_review_already_created")},
                409,
            )
        review.user_id = user
        review.product_id = product_id
        review.save_to_db()
        return (
            {
                "message": gettext("product_review_created"),
                "data": product_review_schema.dump(review),
            },
            201,
        )

    @classmethod
    @jwt_required
    def put(cls, product_id):
        user = get_jwt_identity()
        req_data = request.get_json()
        review = product_review_schema.load(
            req_data,
            instance=ReviewModel.get_item(user_id=user, product_id=product_id),
            partial=True,
        )
        if not review.get("id"):
            return {"message": gettext("product_review_already_created")}, 409
        review.save_to_db()
        return (
            {
                "message": gettext("product_review_updated"),
                "data": product_review_schema.dump(review),
            },
            200,
        )

    @classmethod
    @jwt_required
    def delete(cls, product_id):
        user = get_jwt_identity()
        review = ReviewModel.get_item(user_id=user, product_id=product_id)
        if not review:
            return {"message": gettext("product_review_not_found")}, 409
        review.deactivate()
        review.save_to_db()
        return {"message": gettext("product_review_deleted")}, 200


class ProductReviews(Resource):
    @classmethod
    def get(cls, product_id):
        reviews = ReviewModel.get_items(product_id=product_id)
        return (
            {"Reviews": [product_review_schema.dump(review) for review in reviews]},
            200,
        )
