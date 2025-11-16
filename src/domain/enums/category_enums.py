from enum import Enum


class CategoryType(Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME_APPLIANCES = "home_appliances"
    BOOKS = "books"
    TOYS = "toys"

class CategoryStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"

class CategoryVisibility(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"

class CategorySortOrder(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"

class CategoryFilterOption(Enum):
    FEATURED = "featured"
    NEW_ARRIVALS = "new_arrivals"
    BEST_SELLERS = "best_sellers"
    ON_SALE = "on_sale"

class CategoryDisplayMode(Enum):
    GRID = "grid"
    LIST = "list"
    CAROUSEL = "carousel"

class CategoryPromotionType(Enum):
    DISCOUNT = "discount"
    BUNDLE = "bundle"
    FLASH_SALE = "flash_sale"