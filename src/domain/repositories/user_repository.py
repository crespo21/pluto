from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User
from ..enums.user_enums import UserStatus

class UserRepository(ABC):
    """
    Abstract repository interface defining complete CRUD operations for User entities.
    This interface ensures separation of concerns between domain logic and data persistence.
    """
    
    # CREATE operations
    @abstractmethod
    def create(self, user: User) -> User:
        """
        Create a new user in the repository.
        
        Args:
            user: User entity to create
            
        Returns:
            User: Created user with generated ID
            
        Raises:
            UserAlreadyExistsError: If user with same username/email exists
        """
        pass
    
    @abstractmethod
    def bulk_create(self, users: List[User]) -> List[User]:
        """
        Create multiple users in a single transaction.
        
        Args:
            users: List of User entities to create
            
        Returns:
            List[User]: Created users with generated IDs
        """
        pass
    
    # READ operations
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Find user by unique identifier.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Find user by username.
        
        Args:
            username: Unique username
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find user by email address.
        
        Args:
            email: Unique email address
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        """
        Retrieve all users with optional pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List[User]: List of users
        """
        pass
    
    @abstractmethod
    def find_by_status(self, status: 'UserStatus', limit: Optional[int] = None) -> List[User]:
        """
        Find users by status with optional limit.
        
        Args:
            status: User status to filter by
            limit: Maximum number of users to return
            
        Returns:
            List[User]: List of users with specified status
        """
        pass
    
    @abstractmethod
    def count_total(self) -> int:
        """
        Get total count of users in repository.
        
        Returns:
            int: Total number of users
        """
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """
        Check if user exists by username.
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        Check if user exists by email.
        
        Args:
            email: Email to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        pass
    
    # UPDATE operations
    @abstractmethod
    def update(self, user: User) -> User:
        """
        Update existing user in repository.
        
        Args:
            user: User entity with updated data
            
        Returns:
            User: Updated user entity
            
        Raises:
            UserNotFoundError: If user doesn't exist
        """
        pass
    
    @abstractmethod
    def update_partial(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Partially update user with specific fields.
        
        Args:
            user_id: User identifier
            **kwargs: Fields to update
            
        Returns:
            Optional[User]: Updated user if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_status(self, user_id: int, status: 'UserStatus') -> Optional[User]:
        """
        Update user status specifically.
        
        Args:
            user_id: User identifier
            status: New status to set
            
        Returns:
            Optional[User]: Updated user if found, None otherwise
        """
        pass
    
    # DELETE operations
    @abstractmethod
    def delete_by_id(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def delete_by_username(self, username: str) -> bool:
        """
        Delete user by username.
        
        Args:
            username: Username to delete
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        pass
    
    @abstractmethod
    def soft_delete(self, user_id: int) -> Optional[User]:
        """
        Soft delete user (mark as inactive/deleted without removing from database).
        
        Args:
            user_id: User identifier
            
        Returns:
            Optional[User]: Updated user if found, None otherwise
        """
        pass
    
    @abstractmethod
    def bulk_delete(self, user_ids: List[int]) -> int:
        """
        Delete multiple users by their IDs.
        
        Args:
            user_ids: List of user identifiers
            
        Returns:
            int: Number of users successfully deleted
        """
        pass
    
    @abstractmethod
    def delete_all(self) -> int:
        """
        Delete all users from repository.
        WARNING: Use with extreme caution.
        
        Returns:
            int: Number of users deleted
        """
        pass