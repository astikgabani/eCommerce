from resources.address import Address
from resources.cart import Cart, CartItem, ApplyCoupon, MergeTwoCart
from resources.coupons import Coupon, Coupons, ProductCouponMapping
from resources.order import (
    Order,
    OrderCreate,
    Orders,
    OrderReceiver,
    OrderReceiverCreate,
)
from resources.product_category import ProductCategory, ProductCategoryCreate
from resources.products import (
    Product,
    Products,
    ProductCreate,
    ProductAttribute,
    ProductAttributeCreate,
    ProductAttributes,
    ProductAttributeOption,
    ProductAttributeOptions,
    ProductAttributeOptionCreate,
    ProductImages,
    ProductImage,
)
from resources.review import ProductReview, ProductReviews
from resources.users import (
    UserLogin,
    UserRegister,
    UserRoles,
    UserFreshLogin,
    UserTokenRefresh,
    UserRoleAssign,
    UserEmailConfirm,
    UserEmailConfirmByUser,
)


def add_resources(api):

    # address
    api.add_resource(Address, "/address")

    # cart
    api.add_resource(Cart, "/cart")
    api.add_resource(CartItem, "/cart-item")
    api.add_resource(ApplyCoupon, "/apply-coupon/<string:coupon_code>")
    api.add_resource(MergeTwoCart, "/cart-merge/<int:cart_id>")

    # coupon
    api.add_resource(Coupon, "/coupon/<string:code>")
    api.add_resource(Coupons, "/coupons")
    api.add_resource(ProductCouponMapping, "/coupon-product-mapping/<string:code>")

    # order
    api.add_resource(OrderCreate, "/order")
    api.add_resource(Orders, "/orders")
    api.add_resource(Order, "/order/<string:order_id>")
    api.add_resource(OrderReceiverCreate, "/order-receiver")
    api.add_resource(OrderReceiver, "/order-receiver/<int:id>")

    # product category
    api.add_resource(ProductCategory, "/product-category/<int:id>")
    api.add_resource(ProductCategoryCreate, "/product-categories/<int:parent_id>")

    # product
    api.add_resource(Product, "/product/<string:slug>")
    api.add_resource(ProductCreate, "/product")
    api.add_resource(Products, "/products")
    # product attributes
    api.add_resource(ProductAttribute, "/product-attribute/<int:attr_id>")
    api.add_resource(ProductAttributeCreate, "/product-attribute")
    api.add_resource(ProductAttributes, "/product-attributes/<string:slug>")
    # product attributes options
    api.add_resource(ProductAttributeOption, "/product-attribute-option/<int:opt_id>")
    api.add_resource(ProductAttributeOptionCreate, "/product-attribute-option")
    api.add_resource(
        ProductAttributeOptions, "/product-attribute-options/<int:attr_id>"
    )
    # product image
    api.add_resource(ProductImage, "/product-image/<string:slug>/<string:filename>")
    api.add_resource(ProductImages, "/product-image/<string:slug>")

    # product review
    api.add_resource(ProductReview, "/product-review/<int:product_id>")
    api.add_resource(ProductReviews, "/product-reviews/<int:product_id>")

    # user
    api.add_resource(UserLogin, "/login")
    api.add_resource(UserRegister, "/register")
    api.add_resource(UserRoles, "/user-roles")
    api.add_resource(UserRoleAssign, "/user-roles-assign")
    api.add_resource(UserFreshLogin, "/fresh-login")
    api.add_resource(UserTokenRefresh, "/user-token-refresh")
    api.add_resource(UserEmailConfirm, "/user-email-confirm/<string:confirmation_id>")
    api.add_resource(UserEmailConfirmByUser, "/confirm-email-resend/<int:user_id>")
