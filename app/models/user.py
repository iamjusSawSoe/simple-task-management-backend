from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    """
    User model representing registered users in the system.
    
    Attributes:
        id: Primary key
        email: Unique email address
        username: User's display name
        hashed_password: Bcrypt hashed password
        created_at: Timestamp of user creation
        tasks: Relationship to user's tasks
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")