from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    """Service layer for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with hashed password."""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def create_token(self, user_id: int) -> str:
        """Create JWT access token for user."""
        access_token = create_access_token(data={"sub": str(user_id)})
        return access_token