from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.user import User
from app.api.dependencies import get_current_user
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    priority_filter: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks for the authenticated user with optional filtering.
    
    Args:
        status_filter: Optional status filter (pending/in-progress/completed)
        priority_filter: Optional priority filter (low/medium/high)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[TaskResponse]: List of user's tasks
    """
    task_service = TaskService(db)
    tasks = task_service.get_user_tasks(
        current_user.id,
        status_filter=status_filter,
        priority_filter=priority_filter
    )
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single task by ID.
    
    Args:
        task_id: Task ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        TaskResponse: Task details
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
    """
    task_service = TaskService(db)
    task = task_service.get_task_by_id(task_id, current_user.id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.
    
    Args:
        task_data: Task creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        TaskResponse: Created task details
    """
    task_service = TaskService(db)
    new_task = task_service.create_task(task_data, current_user.id)
    return new_task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing task.
    
    Args:
        task_id: Task ID to update
        task_data: Updated task data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        TaskResponse: Updated task details
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
    """
    task_service = TaskService(db)
    updated_task = task_service.update_task(task_id, task_data, current_user.id)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a task.
    
    Args:
        task_id: Task ID to delete
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException 404: If task not found or doesn't belong to user
    """
    task_service = TaskService(db)
    success = task_service.delete_task(task_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return None