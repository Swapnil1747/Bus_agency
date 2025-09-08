# Bus_agency - Online Bus Travel Booking System

Bus_agency is a modern web application for booking bus tickets online. It provides a user-friendly interface for searching, booking, and managing bus tickets.

## Features

- User authentication and authorization
- Search buses by route and date
- Book tickets with seat selection
- View booking history
- Admin panel for bus and route management
- Real-time seat availability
- Email notifications for bookings

## Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: SQLite (development) / PostgreSQL (production)
- Authentication: Flask-Login
- Forms: Flask-WTF

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
6. Run the application:
   ```
   flask run
   ```

## Project Structure

```
Bus_agency/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── main.py
│   ├── static/
│   │   ├── bus-logo.svg
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── img/
│   │   │   └── upi_qr.png
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── book.html
│       ├── booking.html
│       ├── search.html
│       ├── search_results.html
│       ├── my_bookings.html
│       ├── about.html
│       ├── contact.html
│       ├── terms.html
│       ├── admin/
│       │   ├── dashboard.html
│       │   ├── users.html
│       │   ├── buses.html
│       │   ├── routes.html
│       │   ├── bookings.html
│       │   ├── add_bus.html
│       │   ├── add_route.html
│       │   └── _subnav.html
│       └── auth/
│           ├── login.html
│           ├── register.html
│           └── profile.html
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       ├── 1d4f93729d7c_initial_migration.py
│       ├── b287b2be4cb5_add_num_persons_to_booking_model.py
│       ├── cc268032e7e4_add_user_deleted_to_booking_for_soft_.py
│       └── d8b4f63e5b9a_add_upi_reference_and_payment_status_to_.py
├── instance/
├── config.py
├── requirements.txt
├── run.py
├── add_routes.py
├── add_sample_data.py
├── check_db.py
├── create_admin.py
├── db_pro_manager.py
├── init_db.py
├── test_gmail_smtp.py
├── view_users.py
├── .gitignore
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 