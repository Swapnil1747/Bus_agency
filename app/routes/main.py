from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user
from app.models import Route, Bus, Booking, Feedback
from app import db
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from flask import current_app
from flask_mail import Message
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search')
def search():
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    
    routes = []
    if origin and destination and date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d')
            routes = Route.query.filter(
                Route.origin.ilike(f'%{origin}%'),
                Route.destination.ilike(f'%{destination}%'),
                db.func.date(Route.departure_time) == search_date.date()
            ).all()
        except ValueError:
            flash('Invalid date format', 'danger')
    
    return render_template('search.html', routes=routes)

@bp.route('/book/<int:route_id>', methods=['GET', 'POST'])
@login_required
def book(route_id):
    route = Route.query.get_or_404(route_id)
    if request.method == 'POST':
        seat_number = request.form.get('seat_number')
        upi_reference = request.form.get('upi_ref', None)
        num_persons = int(request.form.get('num_persons', 1))
        if not seat_number:
            flash('Please select a seat', 'danger')
            return redirect(url_for('main.book', route_id=route_id))
        # Check if seat is already booked
        existing_booking = Booking.query.filter_by(
            route_id=route_id,
            seat_number=seat_number
        ).first()
        if existing_booking:
            flash('This seat is already booked', 'danger')
            return redirect(url_for('main.book', route_id=route_id))
        booking = Booking(
            user_id=current_user.id,
            route_id=route_id,
            seat_number=seat_number,
            upi_reference=upi_reference,
            payment_status='paid',
            status='confirmed',
            num_persons=num_persons
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful!', 'success')
        return redirect(url_for('main.my_bookings'))
    # Get booked seats for this route
    booked_seats = [b.seat_number for b in route.bookings if b.status == 'confirmed']
    return render_template('book.html', route=route, booked_seats=booked_seats)

@bp.route('/my-bookings')
@login_required
def my_bookings():
    from datetime import datetime
    now = datetime.now()
    # Show all bookings for the current user, regardless of date
    bookings = Booking.query.filter_by(user_id=current_user.id, user_deleted=False).order_by(Booking.booking_date.desc()).all()
    confirmed_bookings = [b for b in bookings if b.status == 'confirmed']
    total_tickets = sum(b.num_persons for b in confirmed_bookings)
    total_spent = sum(b.route.price * b.num_persons for b in confirmed_bookings)
    average_fare = (total_spent / total_tickets) if total_tickets > 0 else 0
    # Show all confirmed tickets, even if user_deleted=True, but only outdated (departure_time < now)
    all_confirmed = Booking.query.join(Route).filter(
        Booking.user_id == current_user.id,
        Booking.status == 'confirmed',
        Route.departure_time < now
    ).order_by(Booking.booking_date.desc()).all()
    return render_template('my_bookings.html', bookings=bookings, total_spent=total_spent, total_tickets=total_tickets, average_fare=average_fare, all_confirmed=all_confirmed)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_text = request.form.get('feedback')
    print('Feedback received:', feedback_text)  # Debug print
    if feedback_text:
        feedback = Feedback(message=feedback_text)
        db.session.add(feedback)
        db.session.commit()
    flash("Thank you for your feedback!", "success")
    return redirect(request.referrer or url_for('main.search'))

@bp.route('/api/search_buses')
def api_search_buses():
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')

    buses = []
    if origin and destination and date:
        try:
            search_date = datetime.strptime(date, '%Y-%m-%d')
            routes = Route.query.filter(
                Route.origin.ilike(f'%{origin}%'),
                Route.destination.ilike(f'%{destination}%'),
                db.func.date(Route.departure_time) == search_date.date()
            ).all()
            for route in routes:
                total_seats = route.bus.capacity
                booked_seats = [b.seat_number for b in route.bookings if b.status == 'confirmed']
                available_seats = total_seats - len(booked_seats)
                buses.append({
                    'id': route.id,
                    'bus_name': route.bus.model,
                    'departure_time': route.departure_time.strftime('%H:%M'),
                    'fare': route.price,
                    'available_seats': available_seats
                })
        except ValueError:
            pass
    return jsonify({'buses': buses})

@bp.route('/book/<int:route_id>/confirm', methods=['POST'])
@login_required
def confirm_booking(route_id):
    route = Route.query.get_or_404(route_id)
    upi_ref = request.form.get('upi_ref', '')
    num_persons = int(request.form.get('num_persons', 1))
    seat_numbers = request.form.getlist('seat_numbers')

    if len(seat_numbers) != num_persons:
        flash('Please select a seat for each person.', 'danger')
        return redirect(url_for('main.book', route_id=route_id))

    # Check for duplicate seats
    if len(set(seat_numbers)) != len(seat_numbers):
        flash('Please select unique seats for each person.', 'danger')
        return redirect(url_for('main.book', route_id=route_id))

    # Check if any seat is already booked
    for seat_number in seat_numbers:
        existing_booking = Booking.query.filter_by(
            route_id=route_id,
            seat_number=seat_number,
            status='confirmed'
        ).first()
        if existing_booking:
            flash(f'Seat {seat_number} is already booked.', 'danger')
            return redirect(url_for('main.book', route_id=route_id))

    # Create a booking for each seat/person
    for seat_number in seat_numbers:
        booking = Booking(
            user_id=current_user.id,
            route_id=route_id,
            seat_number=seat_number,
            upi_reference=upi_ref,
            payment_status='paid',
            status='confirmed',
            num_persons=1
        )
        db.session.add(booking)
    db.session.commit()

    flash('🎉 Booking successful for all selected seats!', 'success')
    return redirect(url_for('main.my_bookings'))

@bp.route('/ticket/<int:booking_id>/pdf')
@login_required
def ticket_pdf(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    route = booking.route
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 100, 730, width=80, height=40, mask='auto')
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Bus Ticket")
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Bus: {route.bus.model}")
    p.drawString(100, 700, f"From: {route.origin}")
    p.drawString(100, 680, f"To: {route.destination}")
    p.drawString(100, 660, f"Departure: {route.departure_time.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 640, f"Arrival: {route.arrival_time.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 620, f"Seat Number: {booking.seat_number}")
    p.drawString(100, 600, f"Fare: ₹{route.price}")
    p.drawString(100, 580, f"Booking Date: {booking.booking_date.strftime('%Y-%m-%d %H:%M')}")
    p.setFont("Helvetica-Bold", 13)
    p.drawString(100, 550, "Thank you for booking with ShrijwalaBus!")
    p.setFont("Helvetica", 11)
    p.drawString(100, 530, "Show this ticket to the bus conductor.")
    p.showPage()
    p.save()
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=bus_ticket.pdf'
    return response

@bp.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('You are not authorized to cancel this booking.', 'danger')
        return redirect(url_for('main.my_bookings'))
    if booking.status == 'cancelled':
        flash('This booking is already cancelled.', 'info')
        return redirect(url_for('main.my_bookings'))
    booking.status = 'cancelled'
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('main.my_bookings'))

@bp.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('You are not authorized to delete this booking.', 'danger')
        return redirect(url_for('main.my_bookings'))
    if booking.status != 'cancelled':
        flash('Only cancelled bookings can be deleted.', 'warning')
        return redirect(url_for('main.my_bookings'))
    booking.user_deleted = True
    db.session.commit()
    flash('Booking deleted from your history.', 'success')
    return redirect(url_for('main.my_bookings'))

@bp.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    # Set user_deleted=True for all bookings for this user (full history)
    Booking.query.filter_by(user_id=current_user.id).update({'user_deleted': True}, synchronize_session=False)
    db.session.commit()
    flash('All booking history cleared from your view.', 'success')
    return redirect(url_for('main.my_bookings'))

@bp.route('/contact/submit', methods=['POST'])
def contact_submit():
    from flask import request, redirect, url_for, flash, current_app
    from flask_mail import Message
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    admin_email = 'swapnilmishrak2230@gmail.com'

    subject = f'Contact Form Submission from {name}'
    body = f"""
    Name: {name}
    Email: {email}
    Message:
    {message}
    """

    mail = current_app.extensions.get('mail')
    if mail is None:
        flash('Email service is not configured. Please contact the admin directly.', 'danger')
        return redirect(url_for('main.contact'))

    try:
        msg = Message(subject, sender=current_app.config.get('MAIL_USERNAME'), recipients=[admin_email])
        msg.body = body
        mail.send(msg)
        flash('Your message has been sent to the admin!', 'success')
    except Exception as e:
        print('Error sending email:', e)
        flash('There was an error sending your message. Please try again later.', 'danger')
    return redirect(url_for('main.contact'))