from db import db

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)

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

roles_users = db.Table('roles_users',
                       db.Column('user_id' , db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id' , db.Integer(), db.ForeignKey('role.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    bookings = db.relationship('Booking', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String, nullable =False)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String, nullable = False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String(255))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    number_of_seats = db.Column(db.Integer, nullable=False)
    show = db.relationship('Show', backref='bookings')
