from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional


class TaskService:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_tasks(
        self,
        user_id: int,
        status_filter: Optional[str] = None,
        priority_filter: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a user with optional filtering.
        Uses optimized query with filters applied at database level.
        
        Args:
            user_id: User's ID
            status_filter: Optional status filter
            priority_filter: Optional priority filter
            
        Returns:
            List of Task objects
        """
        query = self.db.query(Task).filter(Task.user_id == user_id)
        
        if status_filter:
            query = query.filter(Task.status == status_filter)
        
        if priority_filter:
            query = query.filter(Task.priority == priority_filter)
        
        return query.order_by(Task.created_at.desc()).all()
    
    def get_task_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a single task by ID with user authorization check.
        
        Args:
            task_id: Task's ID
            user_id: User's ID for authorization
            
        Returns:
            Task object or None if not found or unauthorized
        """
        return self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()
    
    def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for a user.
        
        Args:
            task_data: Task creation data
            user_id: User's ID
            
        Returns:
            Created Task object
        """
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status.value,
            priority=task_data.priority.value,
            due_date=task_data.due_date,
            user_id=user_id
        )
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        
        return db_task
    
    def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        user_id: int
    ) -> Optional[Task]:
        """
        Update an existing task with partial data.
        
        Args:
            task_id: Task's ID
            task_data: Updated task data (partial)
            user_id: User's ID for authorization
            
        Returns:
            Updated Task object or None if not found/unauthorized
        """
        db_task = self.get_task_by_id(task_id, user_id)
        
        if not db_task:
            return None
        s
        update_data = task_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(value, 'value'):
                value = value.value
            setattr(db_task, field, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        
        return db_task
    
    def delete_task(self, task_id: int, user_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task's ID
            user_id: User's ID for authorization
            
        Returns:
            True if deleted successfully, False if not found/unauthorized
        """
        db_task = self.get_task_by_id(task_id, user_id)
        
        if not db_task:
            return False
        
        self.db.delete(db_task)
        self.db.commit()
        
        return True