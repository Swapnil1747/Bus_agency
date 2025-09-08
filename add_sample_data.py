from app import create_app, db
from app.models import Bus, Route
from datetime import datetime, timedelta

def add_sample_data():
    app = create_app()
    with app.app_context():
        # Add sample buses
        buses = [
            Bus(bus_number="BUS001", model="Volvo B9R", capacity=40),
            Bus(bus_number="BUS002", model="Scania Metrolink", capacity=45),
            Bus(bus_number="BUS003", model="Mercedes-Benz O500", capacity=35),
            Bus(bus_number="BUS004", model="Tata Marcopolo", capacity=50),
            Bus(bus_number="BUS005", model="Ashok Leyland", capacity=42)
        ]
        
        for bus in buses:
            existing_bus = Bus.query.filter_by(bus_number=bus.bus_number).first()
            if not existing_bus:
                db.session.add(bus)
        
        db.session.commit()
        print("Added sample buses!")

        # Add sample routes
        routes = [
            # Mumbai to Pune
            Route(
                origin="Mumbai",
                destination="Pune",
                departure_time=datetime.now() + timedelta(days=1, hours=8),
                arrival_time=datetime.now() + timedelta(days=1, hours=11),
                price=500.00,
                bus_id=1
            ),
            Route(
                origin="Mumbai",
                destination="Pune",
                departure_time=datetime.now() + timedelta(days=1, hours=14),
                arrival_time=datetime.now() + timedelta(days=1, hours=17),
                price=550.00,
                bus_id=2
            ),
            
            # Delhi to Jaipur
            Route(
                origin="Delhi",
                destination="Jaipur",
                departure_time=datetime.now() + timedelta(days=1, hours=9),
                arrival_time=datetime.now() + timedelta(days=1, hours=15),
                price=800.00,
                bus_id=3
            ),
            Route(
                origin="Delhi",
                destination="Jaipur",
                departure_time=datetime.now() + timedelta(days=1, hours=16),
                arrival_time=datetime.now() + timedelta(days=1, hours=22),
                price=850.00,
                bus_id=4
            ),
            
            # Bangalore to Chennai
            Route(
                origin="Bangalore",
                destination="Chennai",
                departure_time=datetime.now() + timedelta(days=1, hours=7),
                arrival_time=datetime.now() + timedelta(days=1, hours=13),
                price=700.00,
                bus_id=5
            )
        ]
        
        for route in routes:
            existing_route = Route.query.filter_by(
                origin=route.origin,
                destination=route.destination,
                departure_time=route.departure_time
            ).first()
            if not existing_route:
                db.session.add(route)
        
        db.session.commit()
        print("Added sample routes!")

if __name__ == '__main__':
    add_sample_data() 