from sqlalchemy.orm import Session
from models import *

# Template CRUD generator for each table
def generate_crud_for(model_class):
    model_name = model_class.__name__.lower()

    def create(db: Session, **kwargs):
        obj = model_class(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def get(db: Session, id: int):
        return db.query(model_class).get(id)

    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(model_class).offset(skip).limit(limit).all()

    def update(db: Session, id: int, **kwargs):
        obj = db.query(model_class).get(id)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(db: Session, id: int):
        obj = db.query(model_class).get(id)
        if not obj:
            return None
        db.delete(obj)
        db.commit()
        return obj

    return {
        f"create_{model_name}": create,
        f"get_{model_name}": get,
        f"get_all_{model_name}": get_all,
        f"update_{model_name}": update,
        f"delete_{model_name}": delete,
    }


# Register CRUD operations for each model
crud = {}
models = [
    Airports, Terminals, Gates, FlightStatuses, PaymentMethods,
    BookingStatuses, Passengers, Flights, FlightSchedules, Bookings,
    Payments, AdminRoles, Admins, Notifications
]

for model in models:
    crud.update(generate_crud_for(model))

# Example usage:
# crud['create_airports'](db, name="LAX", city="Los Angeles", ...)
# crud['get_flights'](db, id=5)
