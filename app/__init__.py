from database import engine
from model import Base
import crud
from database import SessionLocal
from schema import UserCreate
from model import UserRole

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = crud.get_user_by_email(db, "admin@example.com")
        if not admin_user:
            admin_data = UserCreate(
                email="admin@example.com",
                username="admin",
                password="admin123",
                full_name="System Administrator"
            )
            admin_user = crud.create_user(db, admin_data)
            # Set role to admin
            admin_user.role = UserRole.ADMIN
            db.commit()
            print("Default admin user created: admin@example.com / admin123")
        else:
            print("Admin user already exists")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    create_admin_user()