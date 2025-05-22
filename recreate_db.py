from app import app, db

# Drop and recreate all tables
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables have been recreated successfully")
