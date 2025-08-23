from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import models
import schemas
import database
import auth
from database import get_db

# Create FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Security
security = HTTPBearer()

# Helper function to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = auth.verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Auth Routes
@app.post("/auth/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token
    token = auth.create_access_token(data={"user_id": db_user.id})
    return {"user": db_user, "access_token": token, "token_type": "bearer"}

@app.post("/auth/login", response_model=schemas.UserResponse)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Verify user
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token
    token = auth.create_access_token(data={"user_id": db_user.id})
    return {"user": db_user, "access_token": token, "token_type": "bearer"}

# Todo Routes
@app.post("/todos", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        due_date=todo.due_date,
        category=todo.category,
        user_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[schemas.Todo])
async def get_todos(skip: int = 0, limit: int = 100, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.user_id == current_user.id).offset(skip).limit(limit).all()
    return todos

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
async def get_todo(todo_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

# Health check
@app.get("/")
async def root():
    return {"message": "Todo API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)