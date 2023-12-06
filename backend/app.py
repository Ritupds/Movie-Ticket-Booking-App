from flask import Flask, request, jsonify, session, send_file, request
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import make_response,render_template
from datetime import datetime, timedelta
from sqlalchemy import or_
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_bcrypt import check_password_hash,Bcrypt
# from worker import celery_init_app
# import task
import os 
from celery.schedules import crontab
from db import db
from celery import Celery
from flask_mail import Mail, Message
from flask_caching import Cache

app = Flask(__name__)
celery=Celery(app.name, broker="redis://localhost:6379/1" , backend= "redis://localhost:6379/2", timezone="Asia/Kolkata")

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://127.0.0.1:6379/0'
    })

app.secret_key=os.urandom(24)
# app.config["SECRET_KEY"]="mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['JWT_SECRET_KEY']='your_secret_key'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAIL_SERVER']='localhost' #mailhog server
app.config['MAIL_PORT'] = 1025 #mailhog port
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'do-not-reply@localhost.com'

mail=Mail(app)

with app.app_context():
    db.init_app(app)
    from models import User, Venue, Show, Booking, Admin
    db.create_all()
    # celery=celery_init_app(app)
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    CORS(app)
    cache.init_app(app)

#celery tasks and jobs

celery.conf.beat_schedule={
    'Daily_reminder': {
        'task': 'app.Daily_remainder',
        'schedule':crontab(hour=18,minute=30)
    },
    'Monthly_report': {
        'task': 'app.Monthly_report',
        'schedule':crontab(day_of_month='1',hour=9,minute=00)
    }
}

@celery.task
def Daily_remainder():
    with app.app_context():
        # celery task to send daily remainder to users who have not done any booking in the last day, where the response will be send to google space with webhook
        bookings=Booking.query.all()
        for booking in bookings:
            s= datetime.now() - timedelta(days=1)
            if booking.booking_time <= s:
                user=User.query.get(booking.user_id)
                response=requests.post("https://chat.googleapis.com/v1/spaces/AAAAOwSzyCM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=m_WAZWPIrHGCTlmjuzQsaZ8nkX36DfkTgAy9fntlPqs",data=json.dumps({"text":f"Hi, {user.name}, Do remember to check out the new shows for today?"}))
                return response.ok
            # else:
            #     return jsonify({'message':'wrong time'})

@celery.task
def Monthly_report():
    with app.app_context():
        for user in User.query.all():
            # Fetch booking data for the user
            bookings = Booking.query.filter_by(user_id=user.id).all()

            msg = Message("Monthly report", recipients=[user.email])
            # msg.body = "This is your monthly report"

            # Define the HTML content using an f-string with Bootstrap classes
            report_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Report</title>
                <!-- Include Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            </head>
            <body>
                <div class="container">
                    <h1>Monthly Report for {user.name}</h1>
                    <table class="table table-striped table-bordered">
                        <thead class="thead-dark">
                            <tr>
                                <th>Booking ID</th>
                                <th>Show ID</th>
                                <th>Number of Seats</th>
                                <th>Show Name</th>
                                <th>Show Date</th>
                                <th>Show Time</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            # Add booking details to the HTML content
            for booking in bookings:
                show = booking.show
                if show:
                    report_html += f"""
                    <tr>
                        <td>{booking.id}</td>
                        <td>{booking.show_id}</td>
                        <td>{booking.number_of_seats}</td>
                        <td>{show.show_name}</td>
                        <td>{show.date}</td>
                        <td>{show.time}</td>
                    </tr>
                    """
            # Complete the HTML content
            report_html += """
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """
            msg.html = report_html
            mail.send(msg)

        return "welcome"


@celery.task
def UserTriggered_Job():
    with app.app_context():
        venues=Venue.query.all()
        with open("venue.csv","w") as f:
            f.write(f"Name,Place,City,Capacity\n")
            for venue in venues:
                f.write(f"{venue.name},{venue.place},{venue.city},{venue.capacity}\n")
        return True        
    

#  route handler for user loader
def user_loader(user_id):
    if User.query.get(int(user_id)) is not None:
        return User.query.get(int(user_id))
    else:
        return None

#  route handler for admin loader
def admin_loader(admin_id):
    if Admin.query.get(int(admin_id)) is not None:
        return Admin.query.get(int(admin_id))
    else:
        return None
    
#  route handler for downloading the csv file
@app.route("/download")
def download():
    UserTriggered_Job.delay()
    return send_file('venue.csv')
 

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

# route handler for admin login
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


# route handler for user registration
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
    user = User.query.filter_by(email=email).first()
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

# route handler for protected routes
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user["email"]}! This is a protected route.'})

# route handler for checking if user is logged in or not
@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    if admin_loader(get_jwt_identity()):
        return jsonify({"status":"success","message":"Admin is logged in",'is_admin': True}), 200
    elif user_loader(get_jwt_identity()):
        return jsonify({"status":"success","message":"User is logged in",'is_admin': False}), 200
    else:
        return jsonify({"status":"error","message":"User is not logged in"}), 401


# the get  and post route handler for venues

    
@app.route('/admindashboard/venues', methods=['GET'])
@jwt_required()
@cache.cached(timeout=20)
def get_all_venues():
    venues = Venue.query.all()
    venue_list = []

    for venue in venues:
        venue_list.append({
            'id': venue.id,
            'name': venue.name,
            'place': venue.place,
            'city': venue.city,
            'capacity': venue.capacity,
        })

    return jsonify({'status': 'success', 'venues': venue_list}), 200

@app.route('/admindashboard/venues', methods=['POST'])
@jwt_required()
def add_venue():
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

    return {'status': 'success', 'message': 'Venue added successfully', 'venue' : {
        'id' : new_venue.id,
        'name' : new_venue.name,
        'place' : new_venue.place,
        'capacity' : new_venue.capacity,
        'city' : new_venue.city
    }}


# route handler for update and delete of venues         
@app.route('/admindashboard/venues/<venue_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_venue(venue_id):
    current_user = admin_loader(get_jwt_identity())
    print(current_user)
    if request.method == "PUT":
        post_data = request.get_json()
        venue = Venue.query.get(venue_id)
        if venue:
            venue.name = post_data.get('name')
            venue.place = post_data.get('place')
            venue.city = post_data.get('city')
            venue.capacity = post_data.get('capacity')
        
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
        return {
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
        }
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
    
# route handler for update and delete of shows
@app.route('/admindashboard/shows/<show_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_show(show_id):
    current_user = admin_loader(get_jwt_identity())
    print(current_user)

    if request.method == "PUT":
        post_data = request.get_json()
        show = Show.query.get(show_id)
        if show:
            show.show_name = post_data.get('show_name')
            show.genre = post_data.get('genre')
            show.rating = post_data.get('rating')
            show.price = post_data.get('price')
            show.date = post_data.get('date')
            show.time = post_data.get('time')
            show.available_seats = post_data.get('available_seats')
            show.venue_id = post_data.get('venue_id')
            
            db.session.commit()
            return {"status": "success", "message": "Show updated successfully"}, 200
        else:
            return {"status": "error", "message": "Show not found"}, 404
            
    elif request.method == 'DELETE':
        show = Show.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return {"status": "success", "message": "Show deleted successfully"}, 200
        else:
            return {"status": "error", "message": "Show not found"}, 404
    else:
        return {"status": "error", "message": "Invalid request method"}, 405


# route handler for search shows 

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

# booking route handler for users

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
                    "user_id":booking.user_id,
                    'id':booking.id,
                    'show_id':booking.show_id,
                    'booking_time':booking.booking_time,
                    'number_of_seats':booking.number_of_seats,
             
                })
        return {'status':'success','bookings':booking_list}
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
            number_of_seats=number_of_seats,
            booking_time=datetime.now()
        )
        current_user=user_loader(get_jwt_identity())
        current_user.bookings.append(new_booking)
        db.session.add(new_booking)
        show.available_seats-=int(number_of_seats)
        db.session.commit()
        return {'status':'success','message':'Booking successful'}
    
    
#route handler for single show details for bookings (to fetch the show details in the booking information table)

@app.route('/admindashboard/shows/<int:show_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=20)
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

#route handler for testing the celery reminder task    
@app.route('/test')
def test():
    booking=Booking.query.first()
    s= datetime.now() - timedelta(days=1)
    if booking.booking_time <= s:
        return jsonify({'message':booking.booking_time})
    else:
        return jsonify({'message':'wrong time'})

            
if __name__ == "__main__":

    app.run(debug=True)