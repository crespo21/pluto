class CartNotFoundError(Exception):
   pass

class CartItemNotFoundError(Exception):
   pass

class CartAlreadyExistsError(Exception):
   pass

class CartEmptyError(Exception):
   pass

class CartOperationError(Exception):
   pass

class InvalidCartItemError(Exception):
   pass

class CartLimitExceededError(Exception):
   pass