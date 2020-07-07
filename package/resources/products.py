import os
import traceback

from flask import request, send_file
from flask_restful import Resource
from marshmallow import ValidationError
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required

from models.products import (
    ProductModel,
    ProductAttributeModel,
    ProductAttributeOptionsModel,
    ProductImageModel,
)

from schema.products import (
    ProductSchema,
    ProductAttributeSchema,
    ProductAttributeOptionsSchema,
    ProductImageSchema,
    ImageSchema,
    ProductAllSchema,
)

from utils.strings_helper import gettext
from utils.user_roles import required_role
from utils.pagination import paginate

from utils import image_helper

product_schema = ProductSchema()
product_attribute_schema = ProductAttributeSchema()
product_attribute_options_schema = ProductAttributeOptionsSchema()
product_image_schema = ProductImageSchema()
image_schema = ImageSchema()
product_all_schema = ProductAllSchema()


class Product(Resource):
    def get(self, slug):
        product = ProductModel.get_item(slug=slug)
        return product_schema.dump(product), 200

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def put(self, slug):
        req_data = request.get_json()
        product = product_schema.load(
            req_data, instance=ProductModel.get_item(slug=slug), partial=True
        )
        if not product.get("id"):
            return {"message": gettext("product_not_found")}
        product.save_to_db()
        return (
            {
                "message": gettext("product_updated"),
                "data": product_schema.dump(product),
            },
            200,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def delete(self, slug):
        product = ProductModel.get_item(slug=slug)
        if not product:
            return {"message": gettext("product_not_found")}
        product.deactivate()
        product.save_to_db()
        return {"message": gettext("product_deleted")}, 201


class ProductCreate(Resource):
    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self):
        req_data = request.get_json()
        product = product_schema.load(req_data)
        if product.id:
            return {"message": gettext("product_already_found")}
        product.save_to_db()
        return (
            {
                "message": gettext("product_created"),
                "data": product_schema.dump(product),
            },
            200,
        )


class Products(Resource):

    @classmethod
    @paginate("products", schema=product_all_schema)
    def get(cls):
        return ProductModel.get_active()

    @classmethod
    def post(cls):
        """
        You need to provide the data of products as mention below
        ::Example::
        {
            "products": [{
                "name": "shirts",
                "description": "Awesome Shirts",
                "price": 100,
                "attrs": [{
                    "name": "color",
                    "attrs_options": [{
                        "name": "Red",
                        "value": "red",
                        "price_change": 10
                    },
                    {
                        "name": "Blue",
                        "value": "blue",
                        "price_change": 5
                    }]
                }]
            }]
        }
        :return: List of all the products which has not been created successfully.
        {
            "error_products": []
        }
        """
        req_data = request.get_json()
        products_data = req_data.get("products")
        if not isinstance(products_data, list):
            return {"message": gettext("products_should_list")}, 400
        error_lst = []
        for product in products_data:
            try:
                product = product_all_schema.load(product)
            except ValidationError as e:
                error_lst.append((product, str(e)))
                print(e)
                continue
            if product.id:
                error_lst.append((product, gettext("product_already_found")))
                continue
            product.save_to_db()
        return {"error_products": [err_product for err_product in error_lst]}, 200


class ProductAttribute(Resource):
    def get(self, attr_id):
        product_attr = ProductAttributeModel.get_item(id=attr_id)
        return product_attribute_schema.dump(product_attr), 200

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def put(self, attr_id):
        req_data = request.get_json()
        product_attr = product_attribute_schema.load(
            req_data, instance=ProductAttributeModel.get_item(id=attr_id), partial=True
        )
        if not product_attr.get("id"):
            return {"message": gettext("product_attribute_not_found")}
        product_attr.save_to_db()
        return (
            {
                "message": gettext("product_attribute_updated"),
                "data": product_attribute_schema.dump(product_attr),
            },
            200,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def delete(self, attr_id):
        product_attr = ProductAttributeModel.get_item(id=attr_id)
        if not product_attr.get("id"):
            return {"message": gettext("product_attribute_not_found")}
        product_attr.deactivate()
        product_attr.save_to_db()
        return {"message": gettext("product_attribute_deleted")}, 200


class ProductAttributeCreate(Resource):
    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self):
        req_data = request.get_json()
        product_attr = product_attribute_schema.load(
            req_data,
            instance=ProductAttributeModel.get_item(
                product_id=req_data.get("product_id")
            ),
        )
        if product_attr.get("id"):
            return {"message": gettext("product_attribute_not_found")}
        product_attr.save_to_db()
        return (
            {
                "message": gettext("product_attribute_created"),
                "data": product_attribute_schema.dump(product_attr),
            },
            200,
        )


class ProductAttributes(Resource):
    @classmethod
    @required_role(["admin", "shop_keeper"])
    def get(cls, slug):
        product = ProductModel.get_item(slug=slug)
        return (
            {
                "product": product_schema.dump(product),
                "Product Attribute": [
                    product_attribute_schema.dump(product_attr)
                    for product_attr in (product.get("attrs") if product else [])
                ],
            },
            200,
        )


class ProductAttributeOption(Resource):
    def get(self, opt_id):
        product_attr_opt = ProductAttributeOptionsModel.get_item(id=opt_id)
        return product_attribute_options_schema.dump(product_attr_opt), 200

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def put(self, opt_id):
        req_data = request.get_json()
        product_attr_opts = product_attribute_options_schema.load(
            req_data,
            instance=ProductAttributeOptionsModel.get_item(id=opt_id),
            partial=True,
        )
        if not product_attr_opts.id:
            return {"message": gettext("product_attribute_option_not_found")}
        product_attr_opts.save_to_db()
        return (
            {
                "message": gettext("product_attribute_option_updated"),
                "data": product_attribute_options_schema.dump(product_attr_opts),
            },
            200,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def delete(self, opt_id):
        product_attr_opts = ProductAttributeOptionsModel.get_item(id=opt_id)
        if not product_attr_opts:
            return {"message": gettext("product_attribute_option_not_found")}
        product_attr_opts.deactivate()
        product_attr_opts.save_to_db()
        return {"message": gettext("product_attribute_option_deleted")}, 200


class ProductAttributeOptionCreate(Resource):
    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self):
        req_data = request.get_json()
        product_attr_opts = product_attribute_options_schema.load(req_data)
        product_attr_opts.save_to_db()
        return (
            {
                "message": gettext("product_attribute_option_created"),
                "data": product_attribute_options_schema.dump(product_attr_opts),
            },
            200,
        )


class ProductAttributeOptions(Resource):
    @classmethod
    def get(cls, attr_id):
        product_attribute = ProductAttributeModel.get_item(id=attr_id)
        return (
            {
                "product_attribute": product_attribute_schema.dump(product_attribute),
                "Product Attribute Options": [
                    product_attribute_options_schema.dump(opts)
                    for opts in product_attribute.get("attrs_options")
                ],
            },
            200,
        )


class ProductImages(Resource):
    def get(self, slug):
        product_images = ProductImageModel.get_items(product_slug=slug)
        return (
            {
                "Product Images": [
                    product_image_schema.dump(image)
                    if image_helper.is_file_safe(
                        image.get("image_name"), folder=f"product_{slug}"
                    )
                    else image.delete_from_db() or None
                    for image in product_images
                ]
            },
            200,
        )

    @jwt_required
    @required_role(["admin", "shop_keeper"])
    def post(self, slug):
        image_list = list(request.files.listvalues())[0]
        if not len(image_list):
            return {"message": gettext("image_not_found")}, 400
        not_allowed_exts = []
        for image in image_list:
            image_instance = image_schema.load({"image": image})
            folder = f"product_{slug}"
            try:
                image_path = image_helper.save_image(
                    image_instance.get("image"), folder=folder
                )
                basename = image_helper.get_basename(image_path)
                instance = product_image_schema.load({"image_name": basename})
                instance.product_slug = slug
                instance.save_to_db()
            except UploadNotAllowed:
                extension = image_helper.get_extension(image_instance)
                not_allowed_exts.append(f"{extension}")
        return_msg = gettext("image_uploaded").format(
            len(image_list) - len(not_allowed_exts)
        )
        return (
            {
                "message": return_msg
                if not len(not_allowed_exts)
                else return_msg
                + gettext("image_ext_not_allowed").format(", ".join(not_allowed_exts))
            },
            200,
        )


class ProductImage(Resource):
    def get(self, slug, filename: str):
        image = ProductImageModel.get_item(product_slug=slug, image_name=filename)
        folder = f"product_{slug}"
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_filename_illegal")}, 400
        if not image_helper.is_file_safe(filename, folder=folder):
            return {"message": gettext("image_not_found_at_server")}, 400
        if not image:
            return {"message": gettext("image_not_registered")}, 404
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404

    @jwt_required
    def delete(self, slug, filename):
        if not image_helper.is_filename_safe(filename):
            return {"message": gettext("image_not_found")}, 404

        try:
            image = ProductImageModel.get_item(product_slug=slug, image_name=filename)
            image.delete_from_db()
            os.remove(image_helper.get_path(filename, folder=f"product_{slug}"))
            return {"message": gettext("image_deleted")}, 200
        except FileNotFoundError:
            return {"message": gettext("image_not_found")}, 404
        except Exception:
            traceback.print_exc()
            return {"message": gettext("image_deletion_failed")}, 500
