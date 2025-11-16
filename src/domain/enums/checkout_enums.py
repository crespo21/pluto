from enum import Enum

class CheckoutStatus(Enum):
   PENDING = "pending"
   COMPLETED = "completed"
   CANCELLED = "cancelled"
   FAILED = "failed"

