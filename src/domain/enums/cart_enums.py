from enum import Enum

class CartStatus(Enum):
   ADD_TO_CART = "added to cart"
   REMOVED_FROM_CART = "removed from cart"
   PURCHASED = "purchased"
   

class CartAction(Enum):
   ADD = "add"
   REMOVE = "remove"
   UPDATE = "update"
   CHECKOUT = "checkout"
   VIEW = "view"
   CLEAR = "clear"
   
class CartError(Enum):
   OUT_OF_STOCK = "product is out of stock"
   INVALID_PRODUCT = "invalid product"
   CART_EMPTY = "cart is empty"
   PAYMENT_FAILED = "payment failed"
   UNKNOWN_ERROR = "unknown error occurred"

