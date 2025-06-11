from sqlmodel import Session, select
from database import engine
from models import User
from auth import get_password_hash, verify_password

def migrate_passwords():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        
        for user in users:
            try:
                verify_password("test", user.password)
                print(f"User {user.username} already has hashed password")
            except:
                print(f"Hashing password for user {user.username}")
                hashed_password = get_password_hash(user.password)
                user.password = hashed_password
                session.add(user)
        
        session.commit()
        print("Password migration completed!")

if __name__ == "__main__":
    migrate_passwords() 