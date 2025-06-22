# server/seed.py

from app import app, db
from models import Plant # Import your Plant model

with app.app_context():
    print("Clearing existing data...")
    Plant.query.delete() # Clear existing plants

    print("Creating seed data...")
    plants_data = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
        Plant(name="Fiddle Leaf Fig", image="./images/fiddle_leaf_fig.jpg", price=25.00, is_in_stock=True),
        Plant(name="Snake Plant", image="./images/snake_plant.jpg", price=18.75, is_in_stock=False),
        Plant(name="Pothos", image="./images/pothos.jpg", price=10.00, is_in_stock=True),
        Plant(name="Monstera", image="./images/monstera.jpg", price=30.00, is_in_stock=True),
        Plant(name="Peace Lily", image="./images/peace_lily.jpg", price=15.00, is_in_stock=False),
    ]

    db.session.add_all(plants_data)
    db.session.commit()

    print("Seed data created successfully!")