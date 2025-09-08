from app import create_app, db
from app.models import User

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin = User(
            username='admin',
            email='admin@swiftbus.com',
            is_admin=True
        )
        admin.set_password('admin123')  # You should change this password

        # Add to database
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin_user() 