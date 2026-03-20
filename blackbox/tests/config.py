BASE_URL = "http://localhost:8080/api/v1"

ROLL_NUMBER = 2024101098
USER_ID = 1

DEFAULT_HEADERS = {
    "X-Roll-Number": ROLL_NUMBER,
    "X-User-ID": USER_ID,
}

ADMIN_HEADERS = {
    "X-Roll-Number": ROLL_NUMBER,
}

INVALID_HEADERS = {
    "X-Roll-Number": "invalid",
    "X-User-ID": "invalid",
}

PROFILE_ENDPOINT = "/profile"
ADDRESS_ENDPOINT = "/addresses"
PRODUCT_ENDPOINT = "/products"
CART_ENDPOINT = "/cart"
COUPON_ENDPOINT = "/coupon"
CHECKOUT_ENDPOINT = "/checkout"
WALLET_ENDPOINT = "/wallet"
LOYALTY_ENDPOINT = "/loyalty"
ORDER_ENDPOINT = "/orders"
SUPPORT_ENDPOINT = "/support/tickets"