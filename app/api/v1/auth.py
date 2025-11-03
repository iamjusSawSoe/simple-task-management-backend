from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, username, password)
        db: Database session
        
    Returns:
        UserResponse: Created user information (without password)
        
    Raises:
        HTTPException 400: If email already registered
    """
    auth_service = AuthService(db)
    
    existing_user = auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = auth_service.create_user(user_data)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    Args:
        login_data: User login credentials (email, password)
        db: Database session
        
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    auth_service = AuthService(db)
    
    # Authenticate user
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_token(user.id)
    
    return Token(access_token=access_token)