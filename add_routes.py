from app import create_app, db
from app.models import Route, Bus
from datetime import datetime, timedelta

def add_sample_routes():
    app = create_app()
    with app.app_context():
        # Get all buses
        buses = Bus.query.all()
        if not buses:
            print("No buses found in the database!")
            return

        # Sample routes data
        routes_data = [
            {
                'origin': 'Mumbai',
                'destination': 'Pune',
                'departure_time': datetime.now() + timedelta(days=1, hours=8),  # 8 AM tomorrow
                'arrival_time': datetime.now() + timedelta(days=1, hours=11),   # 11 AM tomorrow
                'price': 500.00,
                'bus': buses[0]  # Volvo B9R
            },
            {
                'origin': 'Mumbai',
                'destination': 'Nashik',
                'departure_time': datetime.now() + timedelta(days=1, hours=10),
                'arrival_time': datetime.now() + timedelta(days=1, hours=14),
                'price': 600.00,
                'bus': buses[1]  # Scania K360
            },
            {
                'origin': 'Pune',
                'destination': 'Mumbai',
                'departure_time': datetime.now() + timedelta(days=1, hours=14),
                'arrival_time': datetime.now() + timedelta(days=1, hours=17),
                'price': 500.00,
                'bus': buses[2]  # Mercedes-Benz O500
            },
            {
                'origin': 'Mumbai',
                'destination': 'Goa',
                'departure_time': datetime.now() + timedelta(days=2, hours=20),
                'arrival_time': datetime.now() + timedelta(days=3, hours=8),
                'price': 1200.00,
                'bus': buses[0]  # Volvo B9R
            }
        ]

        # Add routes to database
        for route_data in routes_data:
            route = Route(**route_data)
            db.session.add(route)
        
        try:
            db.session.commit()
            print("Sample routes added successfully!")
            
            # Display added routes
            print("\nAdded Routes:")
            routes = Route.query.all()
            for route in routes:
                print(f"- {route.origin} to {route.destination}")
                print(f"  Departure: {route.departure_time}")
                print(f"  Arrival: {route.arrival_time}")
                print(f"  Price: ₹{route.price}")
                print(f"  Bus: {route.bus.bus_number} ({route.bus.model})")
                print()
                
        except Exception as e:
            db.session.rollback()
            print(f"Error adding routes: {str(e)}")

if __name__ == '__main__':
    add_sample_routes() 