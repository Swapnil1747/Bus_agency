import sqlite3
from tabulate import tabulate
import os
from datetime import datetime, timedelta
import getpass

class ProfessionalDBManager:
    def __init__(self, db_name='swiftbus.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.current_user = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # This enables column access by name
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to {self.db_name}")
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def login(self):
        print("\n=== Admin Login ===")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        query = "SELECT * FROM user WHERE username = ? AND is_admin = 1"
        user = self.fetch_one(query, (username,))
        
        if user and user['password_hash'] == password:  # In real app, use proper password hashing
            self.current_user = user
            print(f"Welcome, {user['username']}!")
            return True
        else:
            print("Invalid credentials or insufficient privileges!")
            return False

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False

    def fetch_all(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def view_table(self, table_name):
        columns = [col[1] for col in self.get_table_info(table_name)]
        data = self.fetch_all(f"SELECT * FROM {table_name}")
        
        if data:
            print(f"\n=== {table_name.upper()} TABLE ===")
            print(tabulate(data, headers=columns, tablefmt="grid"))
            print(f"\nTotal records: {len(data)}")
        else:
            print(f"\nNo data found in {table_name} table")

    def get_table_info(self, table_name):
        return self.fetch_all(f"PRAGMA table_info({table_name})")

    def add_bus(self):
        print("\n=== Add New Bus ===")
        bus_number = input("Bus Number: ")
        model = input("Model: ")
        capacity = int(input("Capacity: "))
        
        query = "INSERT INTO bus (bus_number, model, capacity) VALUES (?, ?, ?)"
        if self.execute_query(query, (bus_number, model, capacity)):
            print("Bus added successfully!")

    def add_route(self):
        print("\n=== Add New Route ===")
        origin = input("Origin: ")
        destination = input("Destination: ")
        departure_time = input("Departure Time (YYYY-MM-DD HH:MM): ")
        arrival_time = input("Arrival Time (YYYY-MM-DD HH:MM): ")
        price = float(input("Price: "))
        bus_id = int(input("Bus ID: "))
        
        query = """INSERT INTO route (origin, destination, departure_time, arrival_time, price, bus_id) 
                  VALUES (?, ?, ?, ?, ?, ?)"""
        if self.execute_query(query, (origin, destination, departure_time, arrival_time, price, bus_id)):
            print("Route added successfully!")

    def view_bookings(self):
        print("\n=== Bookings Report ===")
        query = """
        SELECT b.id, u.username, r.origin, r.destination, b.seat_number, 
               b.booking_date, b.status, b.payment_status
        FROM booking b
        JOIN user u ON b.user_id = u.id
        JOIN route r ON b.route_id = r.id
        ORDER BY b.booking_date DESC
        """
        bookings = self.fetch_all(query)
        if bookings:
            headers = ['ID', 'User', 'From', 'To', 'Seat', 'Booking Date', 'Status', 'Payment']
            print(tabulate(bookings, headers=headers, tablefmt="grid"))
        else:
            print("No bookings found!")

    def view_route_analytics(self):
        print("\n=== Route Analytics ===")
        query = """
        SELECT r.origin, r.destination, COUNT(b.id) as booking_count,
               AVG(r.price) as avg_price
        FROM route r
        LEFT JOIN booking b ON r.id = b.route_id
        GROUP BY r.origin, r.destination
        """
        analytics = self.fetch_all(query)
        if analytics:
            headers = ['From', 'To', 'Total Bookings', 'Average Price']
            print(tabulate(analytics, headers=headers, tablefmt="grid"))
        else:
            print("No route data found!")

    def backup_database(self):
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        try:
            with open(self.db_name, 'rb') as source:
                with open(backup_name, 'wb') as backup:
                    backup.write(source.read())
            print(f"Database backed up successfully to {backup_name}")
        except Exception as e:
            print(f"Error backing up database: {e}")

def main():
    db = ProfessionalDBManager()
    if db.connect():
        if db.login():
            while True:
                print("\n=== Professional Database Manager ===")
                print("1. View Tables")
                print("2. Add New Bus")
                print("3. Add New Route")
                print("4. View Bookings Report")
                print("5. View Route Analytics")
                print("6. Backup Database")
                print("7. Exit")
                
                choice = input("\nEnter your choice (1-7): ")
                
                if choice == '1':
                    table_name = input("Enter table name to view (user/bus/route/booking): ")
                    db.view_table(table_name)
                
                elif choice == '2':
                    db.add_bus()
                
                elif choice == '3':
                    db.add_route()
                
                elif choice == '4':
                    db.view_bookings()
                
                elif choice == '5':
                    db.view_route_analytics()
                
                elif choice == '6':
                    db.backup_database()
                
                elif choice == '7':
                    break
                
                else:
                    print("Invalid choice!")
        
        db.close()

if __name__ == "__main__":
    main() 