from sqlmodel import Session, select
from database import engine
from models import User

def check_passwords():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print("\nПроверка хешей паролей в базе данных:")
        print("-" * 50)
        for user in users:
            print(f"\nПользователь: {user.username}")
            print(f"Хеш пароля: {user.password}")
            is_hashed = user.password.startswith('$2b$')
            print(f"Пароль захеширован? {'Да' if is_hashed else 'Нет!'}")
            if not is_hashed:
                print("ВНИМАНИЕ: Этот пароль не захеширован!")
        print("\n" + "-" * 50)

if __name__ == "__main__":
    check_passwords() 