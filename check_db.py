import os
import sys
from app import create_app, db
from app.models import User, Bus, Route, Booking
from sqlalchemy import inspect

def check_database():
    app = create_app()
    with app.app_context():
        # Get inspector
        inspector = inspect(db.engine)
        
        # Check user table structure
        print("\nUser Table Structure:")
        for column in inspector.get_columns('user'):
            print(f"- {column['name']}: {column['type']}")
        
        # Check existing users
        print("\nExisting Users:")
        users = User.query.all()
        for user in users:
            print(f"- {user.username} (Admin: {user.is_admin})")
        
        # Check buses
        print("\nExisting Buses:")
        buses = Bus.query.all()
        for bus in buses:
            print(f"- {bus.bus_number}: {bus.model} ({bus.capacity} seats)")
        
        # Check routes
        print("\nExisting Routes:")
        routes = Route.query.all()
        for route in routes:
            print(f"- {route.origin} to {route.destination}")

if __name__ == '__main__':
    check_database() 