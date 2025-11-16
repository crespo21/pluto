class CheckoutException(Exception):
    """Base exception for checkout-related errors."""
    pass

class CheckoutNotFoundError(CheckoutException):
    """Exception raised when a checkout is not found."""
    pass

class InvalidCheckoutDataError(CheckoutException):
    """Exception raised for invalid checkout data."""
    pass 

class CheckoutAlreadyCompletedError(CheckoutException):
    """Exception raised when trying to complete an already completed checkout."""
    pass

