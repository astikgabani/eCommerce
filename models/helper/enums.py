import enum


class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"

    def __str__(self):
        return self.value


class SessionEnum(enum.Enum):
    web = "Web"
    mobile = "Mobile"


class CountryEnum(enum.Enum):
    india = "India"


class AddressTypeEnum(enum.Enum):
    billing = "Billing"
    shipping = "Shipping"


class CouponTypeEnum(enum.Enum):
    percentage = "Percentage"
    price = "Price"


class OrderStatusEnum(enum.Enum):
    shipped = "Shipped"
    placed = "Placed"
    delivered = "Delivered"
    cancelled = "Cancelled"
