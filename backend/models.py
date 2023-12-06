from db import db

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True, cascade="all, delete-orphan")

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String, nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    available_seats = db.Column(db.Integer, default=0, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    bookings = db.relationship('Booking', backref='show', lazy=True, cascade="all, delete-orphan")


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    bookings = db.relationship('Booking', backref='user', lazy=True)
    

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, nullable =False)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    booking_time = db.Column(db.DateTime, nullable = False)
    number_of_seats = db.Column(db.Integer, nullable=False)
    
