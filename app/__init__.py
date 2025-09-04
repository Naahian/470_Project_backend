from app.crud import user_crud as crud
from database import SessionLocal, engine, Base
from app.schema.user_schema import *
#models
from app.model.user_model import *
from app.model.transaction_model import *
from app.model.product_model import *
from app.model.category_model import *
from app.model.supplier_model import *


def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
