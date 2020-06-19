from admin.users import (
    UserView,
    UserRoleView,
    UserSessionView,
    UserSessionTokenView,
    UserConfirmationView,
)
from admin.address import AddressView
from admin.cart import CartView, CartItemView
from admin.coupons import CouponView
from admin.order import OrderView, OrderReceiverView
from admin.product_category import ProductCategoryView
from admin.products import (
    ProductView,
    ProductAttributeView,
    ProductAttributeOptionsView,
    ProductImageView,
)
from admin.review import ReviewView

USER_CATEGORY = "User"
CART_CATEGORY = "Cart"
ORDER_CATEGORY = "Order"
PRODUCT_CATEGORY = "Product"


def add_admin_views(admin):
    admin.add_view(UserView(name="User", category=USER_CATEGORY))
    admin.add_view(UserRoleView(name="User Roles", category=USER_CATEGORY))
    admin.add_view(UserSessionView(name="User Session", category=USER_CATEGORY))
    admin.add_view(
        UserSessionTokenView(name="User Session Tokens", category=USER_CATEGORY)
    )
    admin.add_view(
        UserConfirmationView(name="User Confirmations", category=USER_CATEGORY)
    )

    admin.add_view(AddressView(name="Address"))

    admin.add_view(CartView(name="Cart", category=CART_CATEGORY))
    admin.add_view(CartItemView(name="Cart Items", category=CART_CATEGORY))

    admin.add_view(CouponView(name="Coupons"))

    admin.add_view(OrderView(name="Order", category=ORDER_CATEGORY))
    admin.add_view(OrderReceiverView(name="Order Receiver", category=ORDER_CATEGORY))

    admin.add_view(ProductView(name="Product", category=PRODUCT_CATEGORY))
    admin.add_view(
        ProductAttributeView(name="Product Attributes", category=PRODUCT_CATEGORY)
    )
    admin.add_view(
        ProductAttributeOptionsView(
            name="Product Attribute Options", category=PRODUCT_CATEGORY
        )
    )
    admin.add_view(
        ProductCategoryView(name="Product Category", category=PRODUCT_CATEGORY)
    )
    admin.add_view(ProductImageView(name="Product Images", category=PRODUCT_CATEGORY))
    admin.add_view(ReviewView(name="Product Reviews", category=PRODUCT_CATEGORY))
