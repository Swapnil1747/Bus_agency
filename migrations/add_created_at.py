import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from datetime import datetime
from sqlalchemy import text

def upgrade():
    app = create_app()
    with app.app_context():
        # Add created_at column with default value
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP'))
            conn.commit()
        print("Added created_at column successfully!")

def downgrade():
    app = create_app()
    with app.app_context():
        # Remove created_at column
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE user DROP COLUMN created_at'))
            conn.commit()
        print("Removed created_at column successfully!")

if __name__ == '__main__':
    upgrade() 