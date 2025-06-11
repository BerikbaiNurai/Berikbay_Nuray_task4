from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from models import User
from database import init_db, get_session, engine
from schemas import UserCreate, UserLogin, UserRead, Token
from auth  import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {"sub": db_user.username}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Привет, {current_user}! Это защищенный маршрут."}
