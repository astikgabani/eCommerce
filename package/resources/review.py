from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.review import ReviewModel

from schema.review import ProductReviewSchema

from utils.strings_helper import gettext

product_review_schema = ProductReviewSchema()


class ProductReview(Resource):
    @classmethod
    def get(cls, product_id):
        """
        @param product_id: product unique id
        @type product_id: int

        1. fetch the review data from db
        2. if review not found, return 404 not found
        3. return review details.

        @return: return review details
        @rtype: dict of review details
        """
        review = ReviewModel.get_item(product_id=product_id)
        if not review:
            return {"message": gettext("product_review_not_found")}, 404
        return {"data": product_review_schema.dump(review)}, 200

    @classmethod
    @jwt_required()
    def post(cls, product_id):
        """
        @param product_id: product unique id
        @type product_id: int

        1. load the review data with request data from db
        2. if review found, return 409 conflict
        3. assign user and product, save to db and return newly created review details

        @return: newly created review details
        @rtype: dict of newly created review details
        """
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
    @jwt_required()
    def put(cls, product_id):
        """
        @param product_id: product unique id
        @type product_id: int

        1. load the review data with request data from db
        2. if review not found, return 404 not found
        3. save to db and return updated review details

        @return: updated review details
        @rtype: dict of updated review details
        """
        user = get_jwt_identity()
        req_data = request.get_json()
        review = product_review_schema.load(
            req_data,
            instance=ReviewModel.get_item(user_id=user, product_id=product_id),
            partial=True,
        )
        if not review.get("id"):
            return {"message": gettext("product_review_already_created")}, 404
        review.save_to_db()
        return (
            {
                "message": gettext("product_review_updated"),
                "data": product_review_schema.dump(review),
            },
            200,
        )

    @classmethod
    @jwt_required()
    def delete(cls, product_id):
        """
        @param product_id: product unique id
        @type product_id: int

        1. fetch the review data from db
        2. if review not found, return 404 not found
        3. deactivate, save to db and return proper delete msg

        @return: delete msg
        @rtype: dict of msg
        """
        user = get_jwt_identity()
        review = ReviewModel.get_item(user_id=user, product_id=product_id)
        if not review:
            return {"message": gettext("product_review_not_found")}, 404
        review.deactivate()
        review.save_to_db()
        return {"message": gettext("product_review_deleted")}, 200


class ProductReviews(Resource):
    @classmethod
    def get(cls, product_id):
        """
        @param product_id: product unique id
        @type product_id: int

        Return all the reviews of specific product
        1. load all the review data from db
        2. if review found, return 409 conflict
        3. make the list of all review and return list of review details

        @return: list of review details
        @rtype: dict of listed review details
        """
        reviews = ReviewModel.get_items(product_id=product_id)
        if not reviews:
            return {"message": gettext("product_review_not_found")}, 404
        return (
            {"Reviews": [product_review_schema.dump(review) for review in reviews]},
            200,
        )
