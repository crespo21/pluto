from typing import Optional
from decimal import Decimal
# from datetime import datetime
from src.domain.enums.checkout_enums import CheckoutStatus


class Checkout:
    """
    Represents a user's checkout session for purchasing products.
    Tracks order details, pricing, and checkout status.
    """
    
    def __init__(
        self,
        user_id: int,
        checkout_id: Optional[int] = None,
        product_id: Optional[int] = None,
        quantity: int = 1,
        price: Decimal = Decimal('0.00'),
        total_price: Optional[Decimal] = None,
        status: CheckoutStatus = CheckoutStatus.PENDING,
        # created_at: Optional[datetime] = None,
        # updated_at: Optional[datetime] = None
    ):
        """
        Initialize a Checkout instance.
        
        Args:
            user_id: The ID of the user performing checkout
            checkout_id: Unique identifier for the checkout session
            product_id: The ID of the product being purchased
            quantity: Number of items being purchased
            price: Unit price of the product
            total_price: Total price (quantity × price)
            status: Current checkout status
            created_at: Timestamp when checkout was created
            updated_at: Timestamp of last update
        """
        if user_id is None or user_id <= 0:
            raise ValueError("user_id is required and must be positive")
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        if price < 0:
            raise ValueError("price cannot be negative")
            
        self.checkout_id = checkout_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = max(1, quantity)  # Ensure minimum 1
        self.price = price
        self.total_price = total_price or self.calculate_total()
        self.status = status
        # self.created_at = created_at or datetime.utcnow()
        # self.updated_at = updated_at or datetime.utcnow()

    def calculate_total(self) -> Decimal:
        """Calculate total price based on quantity and unit price."""
        total = self.price * Decimal(str(self.quantity))
        self.total_price = total
        return total

    def validate(self) -> bool:
        """
        Validate checkout data.
        
        Returns:
            True if valid, raises exception if invalid
            
        Raises:
            ValueError: If validation fails
        """
        if self.user_id is None or self.user_id <= 0:
            raise ValueError("Invalid user_id")
        
        # Allow None product_id for pending checkouts (not yet assigned product)
        if self.product_id is not None and self.product_id <= 0:
            raise ValueError("Invalid product_id")
        
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        
        # Allow zero total_price for empty checkouts
        if self.total_price is None or self.total_price < 0:
            raise ValueError("Total price cannot be negative")
        
        return True

    def mark_completed(self) -> None:
        """Mark checkout as completed."""
        self.status = CheckoutStatus.COMPLETED
        # self.updated_at = datetime.utcnow()

    def mark_cancelled(self) -> None:
        """Mark checkout as cancelled."""
        self.status = CheckoutStatus.CANCELLED
        # self.updated_at = datetime.utcnow()

    def mark_failed(self) -> None:
        """Mark checkout as failed."""
        self.status = CheckoutStatus.FAILED
        # self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation of Checkout."""
        return (f"Checkout(id={self.checkout_id}, user_id={self.user_id}, "
                f"product_id={self.product_id}, quantity={self.quantity}, "
                f"total_price={self.total_price}, status={self.status.value})")

    def to_dict(self) -> dict:
        """Convert Checkout to dictionary."""
        return {
            "checkout_id": self.checkout_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": float(self.price),
            "total_price": float(self.total_price) if self.total_price else None,
            "status": self.status.value,
            # "created_at": self.created_at.isoformat() if self.created_at else None,
            # "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
