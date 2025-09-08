from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Bus, Route, Booking, Feedback
from app import db
from datetime import datetime, date, timedelta
from sqlalchemy import func

admin = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_buses = Bus.query.count()
    total_routes = Route.query.count()
    total_bookings = Booking.query.count()
    total_feedback = Feedback.query.count()
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()

    # Total revenue (all time)
    total_revenue = db.session.query(func.sum(Route.price)).join(Booking.route).filter(
        Booking.status == 'confirmed'
    ).scalar() or 0

    # Today's summary stats
    today = date.today()
    todays_bookings = Booking.query.filter(func.date(Booking.booking_date) == today).count()
    todays_revenue = db.session.query(func.sum(Route.price)).join(Booking.route).filter(
        func.date(Booking.booking_date) == today,
        Booking.status == 'confirmed'
    ).scalar() or 0
    todays_users = User.query.filter(func.date(User.created_at) == today).count()

    # 7-day bookings chart
    chart_labels = []
    chart_data = []
    for i in range(7):
        day = today - timedelta(days=6-i)
        chart_labels.append(day.strftime('%a'))
        count = Booking.query.filter(func.date(Booking.booking_date) == day).count()
        chart_data.append(count)

    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_buses=total_buses,
                         total_routes=total_routes,
                         total_bookings=total_bookings,
                         total_feedback=total_feedback,
                         total_revenue=total_revenue,
                         recent_bookings=recent_bookings,
                         todays_bookings=todays_bookings,
                         todays_revenue=todays_revenue,
                         todays_users=todays_users,
                         chart_labels=chart_labels,
                         chart_data=chart_data)

@admin.route('/admin/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

@admin.route('/admin/buses')
@login_required
@admin_required
def buses():
    buses = Bus.query.all()
    return render_template('admin/buses.html', buses=buses)

@admin.route('/admin/routes')
@login_required
@admin_required
def routes():
    routes = Route.query.all()
    return render_template('admin/routes.html', routes=routes)

@admin.route('/admin/bookings')
@login_required
@admin_required
def bookings():
    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)

@admin.route('/admin/add_bus', methods=['GET', 'POST'])
@login_required
@admin_required
def add_bus():
    if request.method == 'POST':
        bus_number = request.form.get('bus_number')
        model = request.form.get('model')
        capacity = request.form.get('capacity')
        
        if not all([bus_number, model, capacity]):
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('admin.add_bus'))
        
        try:
            capacity = int(capacity)
            bus = Bus(bus_number=bus_number, model=model, capacity=capacity)
            db.session.add(bus)
            db.session.commit()
            flash('Bus added successfully!', 'success')
            return redirect(url_for('admin.buses'))
        except ValueError:
            flash('Invalid capacity value', 'danger')
            return redirect(url_for('admin.add_bus'))
    
    return render_template('admin/add_bus.html')

@admin.route('/admin/add_route', methods=['GET', 'POST'])
@login_required
@admin_required
def add_route():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        price = request.form.get('price')
        bus_id = request.form.get('bus_id')
        
        if not all([origin, destination, departure_time, arrival_time, price, bus_id]):
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('admin.add_route'))
        
        try:
            route = Route(
                origin=origin,
                destination=destination,
                departure_time=datetime.strptime(departure_time, '%Y-%m-%dT%H:%M'),
                arrival_time=datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M'),
                price=float(price),
                bus_id=int(bus_id)
            )
            db.session.add(route)
            db.session.commit()
            flash('Route added successfully!', 'success')
            return redirect(url_for('admin.routes'))
        except ValueError:
            flash('Invalid input values', 'danger')
            return redirect(url_for('admin.add_route'))
    
    buses = Bus.query.all()
    return render_template('admin/add_route.html', buses=buses) 