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
        """
        @param slug: slug of product
        @type slug: string

        Get the details of specific product
        1. fetch the details of specific product from the db
        2. return product details

        @return: return product details
        @rtype: dict of product details
        """
        product = ProductModel.get_item(slug=slug)
        if not product:
            return {"data": gettext("product_not_found")}, 404
        return {"data": product_schema.dump(product)}, 200

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def put(self, slug):
        """
        @param slug: slug of product
        @type slug: string

        Update the details of specific product
        1. load the details of specific product from the request data
        2. if product not found, return 404 not found
        3. save to db and return updated product detail

        @return: updated product detail
        @rtype: dict of updated product details
        """
        req_data = request.get_json()
        product = product_schema.load(
            req_data, instance=ProductModel.get_item(slug=slug), partial=True
        )
        if not product.get("id"):
            return {"message": gettext("product_not_found")}, 404
        product.save_to_db()
        return (
            {
                "message": gettext("product_updated"),
                "data": product_schema.dump(product),
            },
            200,
        )

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def delete(self, slug):
        """
        @param slug: slug of product
        @type slug: string

        Delete the details of specific product
        1. fetch the details of specific product from the db
        2. if product not found, return 404 not found
        3. deactivate, save to db and return updated product detail

        @return: updated product detail
        @rtype: dict of updated product details
        """
        product = ProductModel.get_item(slug=slug)
        if not product:
            return {"message": gettext("product_not_found")}, 404
        product.deactivate()
        product.save_to_db()
        return {"message": gettext("product_deleted")}, 200


class ProductCreate(Resource):
    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self):
        """
        Create a product.
        1. load the data based on request data.
        2. if product found, return 409 conflict
        3. save to db and return the newly created product details

        @return: newly created product details
        @rtype: dict of product details
        """
        req_data = request.get_json()
        product = product_schema.load(
            req_data, instance=ProductModel.get_item(slug=req_data.get("slug"))
        )
        if product.id:
            return {"message": gettext("product_already_found")}, 409
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
        """
        Get the list of products
        1. return the all active products.
        (Paginate all this products.)

        @return:
        @rtype:
        """
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

        Create the products by all the json.
        1. loop over the products
        2. load this products, if product found, save to the err_list
        3. save to db and continue in looping
        4. return the error products

        @return: List of all the products which has not been created successfully.
        {
            "error_products": []
        }
        """
        req_data = request.get_json()
        products_data = req_data.get("products")
        if not isinstance(products_data, list):
            return {"message": gettext("products_should_list")}, 400
        error_lst = []
        created_lst = []
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
            created_lst.append(product_all_schema.dump(product))
        return (
            {
                "created_products": [product for product in created_lst],
                "error_products": [err_product for err_product in error_lst],
            },
            200,
        )


class ProductAttribute(Resource):
    def get(self, attr_id):
        """
        @param attr_id: product attribute id
        @type attr_id: int

        Get the detail of product attributes
        1. fetch the product attribute from the db
        2. if attribute not found, return 404 not found
        3. return product attribute details

        @return: return product attribute details
        @rtype: dict of product details
        """
        product_attr = ProductAttributeModel.get_item(id=attr_id)
        if not product_attr:
            return {"message": gettext("product_attribute_not_found")}, 404
        return {"data": product_attribute_schema.dump(product_attr)}, 200

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def put(self, attr_id):
        """
        @param attr_id: product attribute id
        @type attr_id: int

        Update the detail of product attributes
        1. load the product attribute from using product details
        2. if attribute not found, return 404 not found
        3. save to db and return updated product attribute details

        @return: return updated product attribute details
        @rtype: dict of product details
        """
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

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def delete(self, attr_id):
        """
        @param attr_id: product attribute id
        @type attr_id: int

        Get the detail of product attributes
        1. fetch the product attribute from the db
        2. if attribute not found, return 404 not found
        3. deactivate, save to db and return proper delete msg

        @return: return proper delete msg
        @rtype: proper delete msg
        """
        product_attr = ProductAttributeModel.get_item(id=attr_id)
        if not product_attr.get("id"):
            return {"message": gettext("product_attribute_not_found")}
        product_attr.deactivate()
        product_attr.save_to_db()
        return {"message": gettext("product_attribute_deleted")}, 200


class ProductAttributeCreate(Resource):
    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self):
        """
        Create the product attribute.
        1. load the product attribute using request data
        2. if product attribute found, return 409 conflict
        3. save to db and return newly created product attribute details.

        @return: newly created product attribute
        @rtype: dict of product attribute details
        """
        req_data = request.get_json()
        product_attr = product_attribute_schema.load(
            req_data,
            instance=ProductAttributeModel.get_item(
                product_id=req_data.get("product_id")
            ),
        )
        if product_attr.get("id"):
            return {"message": gettext("product_attribute_already_created")}, 409
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
        """
        @param slug: slug of product
        @type slug: string

        Get the list of attributes of specific product
        1. fetch the product from the db
        2. if product not found, return 404 not found
        3. loop over the product's attributes, create a list of that, return this list.

        @return: list of product attributes
        @rtype: dict of list
        """
        product = ProductModel.get_item(slug=slug)
        if not product:
            return {"message": gettext("product_not_found")}, 404
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
        """
        @param opt_id: product attribute option id
        @type opt_id: int

        Get the detail of specific product attribute option details
        1. fetch the product attribute option from the db
        2. if option not found, return 404 not found
        3. return the product attribute option details

        @return: product attribute option details
        @rtype: dict of product attribute option
        """
        product_attr_opt = ProductAttributeOptionsModel.get_item(id=opt_id)
        if not product_attr_opt:
            return {"message": gettext("product_attribute_option_not_found")}, 404
        return {"data": product_attribute_options_schema.dump(product_attr_opt)}, 200

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def put(self, opt_id):
        """
        @param opt_id: product attribute option id
        @type opt_id: int

        Update the detail of specific product attribute option details
        1. load the product attribute option with the request data
        2. if option not found, return 404 not found
        3. save to db and return the updated product attribute option details

        @return: updated product attribute option details
        @rtype: dict of updated product attribute option
        """
        req_data = request.get_json()
        product_attr_opts = product_attribute_options_schema.load(
            req_data,
            instance=ProductAttributeOptionsModel.get_item(id=opt_id),
            partial=True,
        )
        if not product_attr_opts.id:
            return {"message": gettext("product_attribute_option_not_found")}, 404
        product_attr_opts.save_to_db()
        return (
            {
                "message": gettext("product_attribute_option_updated"),
                "data": product_attribute_options_schema.dump(product_attr_opts),
            },
            200,
        )

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def delete(self, opt_id):
        """
        @param opt_id: product attribute option id
        @type opt_id: int

        Delete the detail of specific product attribute option
        1. fetch the product attribute option from the db
        2. if option not found, return 404 not found
        3. deactivate, save to db and return the proper delete msg

        @return: delete msg
        @rtype: dict of deletion msg
        """
        product_attr_opts = ProductAttributeOptionsModel.get_item(id=opt_id)
        if not product_attr_opts:
            return {"message": gettext("product_attribute_option_not_found")}
        product_attr_opts.deactivate()
        product_attr_opts.save_to_db()
        return {"message": gettext("product_attribute_option_deleted")}, 200


class ProductAttributeOptionCreate(Resource):
    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self):
        """
        Create a product attribute option.
        1. load the product attribute option with request data
        2. if product already found, return 409 conflict
        3. save to db and return newly created product attribute option
        @return: newly created product attribute option
        @rtype: dict of newly created item details
        """
        req_data = request.get_json()
        product_attr_opts = product_attribute_options_schema.load(
            req_data,
            instance=ProductAttributeOptionsModel.get_item(name=req_data("name")),
        )
        if product_attr_opts.id:
            return {"message": gettext("product_attribute_option_already_present")}, 409
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
        """
        @param attr_id: product attribute id
        @type attr_id: int

        Get the list of all options of provided product attribute
        1. fetch the product attribute from db
        2. if product attribute not found, return 404 not found
        3. loop over the list of product attribute options and return all these details as list

        @return: product attribute options of given attribute
        @rtype: dict of list
        """
        product_attribute = ProductAttributeModel.get_item(id=attr_id)
        if not product_attribute:
            return {"message": gettext("product_attribute_not_found")}, 404
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
        """
        @param slug: slug of product
        @type slug: string

        Get all the images of given product slug.
        1. fetch the all images from db
        2. if no image found, return 404 not found
        3. loop over the images, if image is safe, add image into the list, else delete the record in db
        4. return this list

        @return: list of all the images of given product
        @rtype: dict of list
        """
        product_images = ProductImageModel.get_items(product_slug=slug)
        if not product_images:
            return {"message": gettext("image_not_registered")}, 404
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

    @jwt_required()
    @required_role(["admin", "shop_keeper"])
    def post(self, slug):
        """
        @param slug: slug of product
        @type slug: string

        Add all the images for given product slug.
        1. Get the list of images from the request.
        2. if no image found, return 404 not found
        3. loop over the image list.
        4. load the image through schema, save image to specific folder and save the data to db
        4. if any error occurred due to invalid file, add this file into error list

        @return: number of image uploaded successfully along with the err msg if err occurred
        @rtype: dict of list
        """
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
        """
        @param slug: slug of product
        @type slug: string
        @param filename: image name
        @type filename: string

        Get specific image of given product
        1. fetch the image data from db.
        2. we are checking for the safe filename, return 400 bad request if found
        3. we are checking for the safe file, return 400 bad request if found
        4. if image not found, return 404 not found.
        5. try to return the image, if image not found, return 404 not found

        @return: image file
        @rtype: image file
        """
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

    @jwt_required()
    def delete(self, slug, filename):
        """
        @param slug: slug of product
        @type slug: string
        @param filename: image name
        @type filename: string

        Delete specific image of given product
        1. fetch the image data from db.
        2. we are checking for the safe filename, return 400 bad request if found
        3. we are checking for the safe file, return 400 bad request if found
        4. if image not found, return 404 not found.
        5. try to return the image, if image not found, return 404 not found

        @return: image file
        @rtype: image file
        """
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
