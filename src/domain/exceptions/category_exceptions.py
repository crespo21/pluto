
class CategoryException(Exception):
    """Base exception for category-related errors."""
    pass

class CategoryNotFoundError(CategoryException):
    """Exception raised when a category is not found."""
    pass

class CategoryAlreadyExistsError(CategoryException):  
    """Exception raised when attempting to create a category that already exists."""
    pass

class InvalidCategoryError(CategoryException):
    """Exception raised for invalid category data."""
    pass 

class CategoryDeletionError(CategoryException):
    """Exception raised when a category cannot be deleted."""
    pass

class CategoryUpdateError(CategoryException):
    """Exception raised when a category cannot be updated."""
    pass

class CategoryAssignmentError(CategoryException):
    """Exception raised when a category cannot be assigned to a product."""
    pass

class CategoryRemovalError(CategoryException):  
    """Exception raised when a category cannot be removed from a product."""
    pass

class CategoryValidationError(CategoryException):  
    """Exception raised for category validation failures."""
    pass

class CategoryDependencyError(CategoryException):
    """Exception raised when a category has dependencies that prevent certain operations."""
    pass

