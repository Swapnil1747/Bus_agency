from app import create_app, db
from app.models import User, Booking, Route, Bus
from tabulate import tabulate

def view_all_data():
    app = create_app()
    with app.app_context():
        # View Users
        print("\n=== USERS ===")
        users = User.query.all()
        if users:
            user_data = []
            for user in users:
                user_data.append([
                    user.id,
                    user.username,
                    user.email,
                    'Yes' if user.is_admin else 'No',
                    user.bookings.count()
                ])
            print(tabulate(user_data, 
                         headers=['ID', 'Username', 'Email', 'Is Admin', 'Total Bookings'],
                         tablefmt="grid"))
        else:
            print("No users found!")

        # View Buses
        print("\n=== BUSES ===")
        buses = Bus.query.all()
        if buses:
            bus_data = []
            for bus in buses:
                bus_data.append([
                    bus.id,
                    bus.bus_number,
                    bus.model,
                    bus.capacity,
                    bus.routes.count()
                ])
            print(tabulate(bus_data,
                         headers=['ID', 'Bus Number', 'Model', 'Capacity', 'Total Routes'],
                         tablefmt="grid"))
        else:
            print("No buses found!")

        # View Routes
        print("\n=== ROUTES ===")
        routes = Route.query.all()
        if routes:
            route_data = []
            for route in routes:
                route_data.append([
                    route.id,
                    route.origin,
                    route.destination,
                    route.departure_time.strftime('%Y-%m-%d %H:%M'),
                    route.arrival_time.strftime('%Y-%m-%d %H:%M'),
                    f"₹{route.price:.2f}",
                    route.bus.bus_number,
                    route.bookings.count()
                ])
            print(tabulate(route_data,
                         headers=['ID', 'From', 'To', 'Departure', 'Arrival', 'Price', 'Bus', 'Bookings'],
                         tablefmt="grid"))
        else:
            print("No routes found!")

        # View Bookings
        print("\n=== BOOKINGS ===")
        bookings = Booking.query.all()
        if bookings:
            booking_data = []
            for booking in bookings:
                booking_data.append([
                    booking.id,
                    booking.user.username,
                    f"{booking.route.origin} → {booking.route.destination}",
                    booking.seat_number,
                    booking.booking_date.strftime('%Y-%m-%d %H:%M'),
                    booking.status,
                    booking.payment_status
                ])
            print(tabulate(booking_data,
                         headers=['ID', 'User', 'Route', 'Seat', 'Booking Date', 'Status', 'Payment'],
                         tablefmt="grid"))
        else:
            print("No bookings found!")

if __name__ == '__main__':
    view_all_data() 