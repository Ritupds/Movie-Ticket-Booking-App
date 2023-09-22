from flask import Flask, request, jsonify, session,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_cors import CORS
from flask import make_response
from datetime import datetime
#from sqlalchemy import or_
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import check_password_hash,Bcrypt
from workers import celery_init_app
import task
import os 
from celery.schedules import crontab

from db import db

app = Flask(__name__)

app.secret_key=os.urandom(24)
# app.config["SECRET_KEY"]="mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['JWT_SECRET_KEY']='your_secret_key'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

with app.app_context():
    db.init_app(app)
    from models import User, Venue, Show, Booking, Admin
    db.create_all()
    celery=celery_init_app(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    CORS(app)
    


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab("*"),
        task.Daily_remainder.s()
        )

# app.app_context().push()
# db.create_all()

def user_loader(user_id):
    if User.query.get(int(user_id)) is not None:
        return User.query.get(int(user_id))
    else:
        return None

def admin_loader(admin_id):
    if Admin.query.get(int(admin_id)) is not None:
        return Admin.query.get(int(admin_id))
    else:
        return None

@app.route("/", methods=['GET'])
def greetings():
    return ("welcome")

@app.route("/landingpage", methods=['GET'])
def landingpage():
    return jsonify ("welcome to your landing page")
 
#  admin registration and login

@app.route('/adminregister', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if Admin.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'admin already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    admin=Admin(name=name, email=email, password=hashed_password)

    db.session.add(admin)
    db.session.commit()
    return jsonify({'status': 'success', 'message' : 'admin registered'}), 201

# Login Route
@app.route('/admin_login', methods=['POST'])
def login():
    if request.method =="POST":
        data=request.get_json()
        email = data['email']
        password = data['password']
        if not email or not password:
            return jsonify({"status":"error","message": "Missing email or password parameter"}), 400

        admin = Admin.query.filter_by(email=email).first()

        if admin:
            if check_password_hash(admin.password, password):
            # Generate the access token for the user
                access_token = create_access_token(identity=admin.id)
                session[admin.id]=admin.id

            # Set is_admin to False for regular users
                is_admin = True

                return jsonify({'access_token': access_token, 'is_admin': is_admin}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Invalid details'}), 401
        else:
            return jsonify({'status': 'error', 'message': 'Admin not found'}), 404
    else:
        return jsonify({"status":"error","message":"Invalid request method"}),405    

# user regitration and login

@app.route('/userregistration', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


    user=User(name=name, email=email, password=hashed_password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'success', 'message' : 'user registered'}), 201
    


# route handler for admin and user login 

@app.route('/user_login', methods=['POST'])
def userlogin():
    email = request.json.get('email')
    password = request.json.get('password')
    # role = request.json.get('role')

    user = User.query.filter_by(email=email).first()

    # if not user or not bcrypt.check_password_hash(user.password, password):
    #     return jsonify({'message': 'Invalid credentials'})
    # if user:
    #     if check_password_hash(user.password,password):
    #         access_token = create_access_token(identity= user.id)
    #         session['user_id']=user.id
    #         return jsonify({'access_token': access_token, 'is_admin': user.is_admin}), 200
    
    #     else: 
    #         return jsonify({'status':'error','message':'invalid details'}), 401
    if user:
        if check_password_hash(user.password, password):
            # Generate the access token for the user
            access_token = create_access_token(identity=user.id)

            # Set is_admin to False for regular users
            is_admin = False

            return jsonify({'access_token': access_token, 'is_admin': is_admin}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid details'}), 401
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user["email"]}! This is a protected route.'})

@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    if admin_loader(get_jwt_identity()):
        return jsonify({"status":"success","message":"Admin is logged in",'is_admin': True}), 200
    elif user_loader(get_jwt_identity()):
        return jsonify({"status":"success","message":"User is logged in",'is_admin': False}), 200
    else:
        return jsonify({"status":"error","message":"User is not logged in"}), 401


# the get  and post route handler

@app.route('/admindashboard/venues', methods=['GET', 'POST'])
@jwt_required()
def all_venues():
    if request.method == "POST":
        current_user = admin_loader(get_jwt_identity())
        print(current_user)
        
            
        post_data = request.get_json()
        new_venue = Venue(
            name=post_data.get('name'),
            place=post_data.get('place'),
            city=post_data.get('city'),
            capacity=post_data.get('capacity'),            
        )
        db.session.add(new_venue)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Venue added successfully'}), 201
        
    else:
        venues = Venue.query.all()
        venue_list = []
        for venue in venues:
            venue_list.append({
                'id': venue.id,
                'name': venue.name,
                'place': venue.place,
                'city': venue.city,
                'capacity': venue.capacity,
                'shows': [show.show_name for show in venue.shows]
            })
        return jsonify({'status': 'success', 'venues': venue_list}), 200
        
@app.route('/admindashboard/venues/<venue_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_venue(venue_id):
    current_user = admin_loader(get_jwt_identity())
    print(current_user)
    # if not current_user.is_admin:
    #     return jsonify({'status': 'error', 'message': 'You are not authorized to perform this action'}), 401

    if request.method == "PUT":
        post_data = request.get_json()
        venue = Venue.query.get(venue_id)
        if venue:
            venue.name = post_data.get('name')
            venue.place = post_data.get('place')
            venue.city = post_data.get('city')
            venue.capacity = post_data.get('capacity')
            # venue.shows=post_data.get('shows')
            
            db.session.commit()
            return jsonify({"status": "success", "message": "Venue updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Venue not found"}), 404
            
    elif request.method == 'DELETE':
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            return jsonify({"status": "success", "message": "Venue deleted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Venue not found"}), 404
            
    else:
        return jsonify({"status": "error", "message": "Invalid request method"}), 405


# Create a route for adding a new show

@app.route('/admindashboard/shows', methods=['GET', 'POST'])
@jwt_required()
def all_shows():

    response_object = {'status': 'success'}
    
    if request.method == "POST":
        current_user = admin_loader(get_jwt_identity())
        print(current_user)
        post_data = request.get_json()
        new_show = Show(
            show_name=post_data.get('show_name'),
            genre=post_data.get('genre'),
            rating=post_data.get('rating'),
            price=post_data.get('price'),
            date=post_data.get('date'),
            time=post_data.get('time'),
            available_seats=post_data.get('available_seats'),
            venue_id=post_data.get('venue_id')
        )
        db.session.add(new_show)
        db.session.commit()
        response_object['message'] = 'Show Added!'
        new_show = Show.query.get(new_show.id)
        return ({
            'id': new_show.id,
            'show_name': new_show.show_name,
            'genre': new_show.genre,
            'rating': new_show.rating,
            'price': new_show.price,
            'date': new_show.date,  
            'time': new_show.time,
            'available_seats': new_show.available_seats,
            'venue': {
                'id': new_show.venue.id,
                'name': new_show.venue.name,
                'place': new_show.venue.place,
                'city': new_show.venue.city
            }
        }),
    else:
        print("hello")
        shows = Show.query.all()
        show_list = []
        for show in shows:
            show_list.append({
                'id': show.id,
                'show_name': show.show_name,
                'genre': show.genre,
                'rating': show.rating,
                'price': show.price,
                'date': show.date,
                'time': show.time,
                'available_seats': show.available_seats,
                'venue': {
                    'id': show.venue.id,
                    'name': show.venue.name,
                    'place': show.venue.place,
                    'city': show.venue.city
                }
                
            })
        print(show_list)    
        return {'status': 'success', 'shows': show_list}, 200
# fetching show details for booking form

@app.route('/admindashboard/shows/<int:show_id>', methods=['GET'])
def get_show_details(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show not found'}), 404
    
    show_details = {
        'id': show.id,
        'show_name': show.show_name,
        'genre': show.genre,
        'rating': show.rating,
        'price': show.price,
        'date': show.date,
        'time': show.time,
        'available_seats': show.available_seats,
        'venue': {
            'id': show.venue.id,
            'name': show.venue.name,
            'place': show.venue.place,
            'city': show.venue.city
        }
    }
    
    return jsonify(show_details), 200


# route handler for update and delete

@app.route('/admindashboard/shows/<show_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_show(show_id):
    current_user = admin_loader(get_jwt_identity())
    print(current_user)
    # if not current_user.is_admin:
    #     return jsonify({'status': 'error', 'message': 'You are not authorized to perform this action'}), 401
    # response_object = {'status': 'success'}

    if request.method == "PUT":
        post_data = request.get_json()
        show = Show.query.get(show_id)
        if show:
            show.show_name = post_data.get('show_name')
            show.genre = post_data.get('genre')
            show.rating = post_data.get('rating')
            show.price = post_data.get('price')
            show.starttime = post_data.get('starttime')
            show.endtime = post_data.get('endtime')
            show.available_seats = post_data.get('available_seats')
            show.venue_id = post_data.get('venue_id')
            
            db.session.commit()
            return jsonify({"status": "success", "message": "Show updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Show not found"}), 404
            
    elif request.method == 'DELETE':
        show = Show.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return jsonify({"status": "success", "message": "Show deleted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Show not found"}), 404
            
    else:
        return jsonify({"status": "error", "message": "Invalid request method"}), 405





@app.route('/logout')
def admin_logout():
    return jsonify({'redirect': '/login'})

#  route handler for users





# search routes
@app.route('/search/venues', methods=['GET'])
def search_venues():
    query = request.args.get('query')
    venues = Venue.query.filter(
        or_(
            Venue.name.ilike(f'%{query}%'),
            Venue.place.ilike(f'%{query}%'),
            Venue.city.ilike(f'%{query}%')
        )
    ).all()

    venue_list = [
        {
            'id': venue.id,
            'name': venue.name,
            'place': venue.place,
            'city': venue.city,
            'capacity': venue.capacity,
            'shows': [show.show_name for show in venue.shows]
        }
        for venue in venues
    ]

    response_object = {'venues': venue_list}
    return jsonify(response_object)

@app.route('/search/shows', methods=['GET'])
def search_shows():
    query = request.args.get('query')
    shows = Show.query.filter(
        Show.show_name.ilike(f'%{query}%')
    ).all()

    show_list = [
        {
            'id': show.id,
            'show_name': show.show_name,
            'genre': show.genre,
            'rating': show.rating,
            'price': show.price,
            'date': show.date,
            'time': show.time,
            'available_seats': show.available_seats,
            'venue': {
                'id': show.venue.id,
                'name': show.venue.name,
                'place': show.venue.place,
                'city': show.venue.city
            }
        }
        for show in shows
    ]

    response_object = {'shows': show_list}
    return jsonify(response_object)

# booking routes for user

@app.route('/bookings', methods=['GET', 'POST'])
@jwt_required()
def all_bookings():
    if request.method=="GET":
        current_user=user_loader(get_jwt_identity())
        if not current_user:
            return jsonify({'status': 'error', 'message': 'You are not authorized to perform this action'}), 401
        bookings=current_user.bookings
        booking_list=[]
        for booking in bookings:
            if booking is not None:
                booking_list.append({
                    'id':booking.id,
                    'show_id':booking.show_id,
                    'number_of_seats':booking.number_of_seats,
                    # 'show_name':booking.show.show_name,
                    # 'venue_name':booking.show.venue.name,
                    # 'venue_place':booking.show.venue.place,
                    # 'venue_city':booking.show.venue.city,
                    # 'date':booking.show.date,
                    # 'time':booking.show.time,
                    # 'price':booking.show.price,
                    # 'total_price':booking.number_of_seats*booking.show.price
                })
            return jsonify({'status':'success','bookings':booking_list}),200
    elif request.method=="POST":
        data=request.get_json()
        show_id=data.get('show_id')
        number_of_seats=data.get('number_of_seats')
        show=Show.query.get(show_id)
        if not show:
            return jsonify({'status':'error','message':'Show not found'}),404
        if show.available_seats<int(number_of_seats):
            return jsonify({'status':'error','message':'Seats not available'}),400
        
        new_booking=Booking(
            show_id=show_id,
            number_of_seats=number_of_seats
        )
        current_user=user_loader(get_jwt_identity())
        current_user.bookings.append(new_booking)
        db.session.add(new_booking)
        show.available_seats-=int(number_of_seats)
        db.session.commit()
        return jsonify({'status':'success','message':'Booking successful'}),201

            
# added functionality for deleting and getting single booking

@app.route('/bookings/<booking_id>', methods=['GET', 'DELETE'])
@jwt_required()
def single_booking(booking_id):
    current_user=user_loader(get_jwt_identity())
    if not current_user:
        return jsonify({'status': 'error', 'message': 'You are not authorized to perform this action'}), 401
    if request.method=="GET":
        booking=Booking.query.get(booking_id)
        if booking is not None:
            return jsonify({
                'id':booking.id,
                'show_id':booking.show_id,
                'number_of_seats':booking.number_of_seats,
                'show_name':booking.show.show_name,
                'venue_name':booking.show.venue.name,
                'venue_place':booking.show.venue.place,
                'venue_city':booking.show.venue.city,
                'date':booking.show.date,
                'time':booking.show.time,
                'price':booking.show.price,
                'total_price':booking.number_of_seats*booking.show.price
            }),200
        else:
            return jsonify({'status':'error','message':'Booking not found'}),404
    elif request.method=="DELETE":
        booking=Booking.query.get(booking_id)
        if booking is not None:
            show=booking.show
            show.available_seats+=booking.number_of_seats
            db.session.delete(booking)
            db.session.commit()
            return jsonify({'status':'success','message':'Booking cancelled'}),200
        else:
            return jsonify({'status':'error','message':'Booking not found'}),404
        

if __name__ == "__main__":

    app.run(debug=True)