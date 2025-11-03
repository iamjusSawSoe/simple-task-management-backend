from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.database import Base


class TaskStatus(str, enum.Enum):
    """Enum for task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(str, enum.Enum):
    """Enum for task priority values"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """
    Task model representing tasks in the system.
    
    Attributes:
        id: Primary key
        title: Task title
        description: Detailed task description
        status: Current status (pending/in-progress/completed)
        priority: Task priority level (low/medium/high)
        due_date: Optional due date
        user_id: Foreign key to user
        created_at: Timestamp of task creation
        updated_at: Timestamp of last update
        owner: Relationship to user
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default=TaskStatus.PENDING.value, nullable=False)
    priority = Column(String, default=TaskPriority.MEDIUM.value, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    owner = relationship("User", back_populates="tasks")