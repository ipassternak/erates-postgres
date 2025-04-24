from app.models.base import Base
from app.models.user import User, UserRole
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.security import hash_password

Base.metadata.create_all(bind=engine)

def create_admin_user(db: Session, email: str, password: str, full_name: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise Exception("admin user with this email already exists")
    hashed_password = hash_password(password)
    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        role=UserRole.ADMIN,
    )
    db.add(new_user)
    db.commit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create an admin user.")
    parser.add_argument("email", type=str, help="Email of the admin user")
    parser.add_argument("password", type=str, help="Password of the admin user")
    parser.add_argument("full_name", type=str, help="Full name of the admin user")
    args = parser.parse_args()
    db = SessionLocal()
    try:
        create_admin_user(db, args.email, args.password, args.full_name)
        print("admin user created successfully")
    except Exception as e:
        print(f"error: {e}")
    finally:
        db.close()
