from app import db, create_app
from app.models import User, Bus, Route, Booking
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@swiftbus.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            created_at=datetime.utcnow()
        )
        
        # Create test user
        test_user = User(
            username='test',
            email='test@example.com',
            password_hash=generate_password_hash('test123'),
            is_admin=False,
            created_at=datetime.utcnow()
        )
        
        # Add users to database
        db.session.add(admin)
        db.session.add(test_user)
        
        # Create sample buses
        buses = [
            Bus(bus_number='BUS001', model='Volvo B9R', capacity=45),
            Bus(bus_number='BUS002', model='Scania K360', capacity=50),
            Bus(bus_number='BUS003', model='Mercedes-Benz O500', capacity=40)
        ]
        
        # Add buses to database
        for bus in buses:
            db.session.add(bus)
        
        # Commit all changes
        db.session.commit()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 