# server/models.py

from app import db # Import the db instance from app.py

class Plant(db.Model):
    __tablename__ = 'plants' # Good practice to explicitly name your table

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True) # Default value for new plants

    # Add any other fields you might have for your Plant model

    def __repr__(self):
        return f'<Plant {self.id}: {self.name}>'

    # Serialization method for converting Plant object to a dictionary (JSON-friendly)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price,
            "is_in_stock": self.is_in_stock
        }