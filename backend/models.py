from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'passenger' or 'driver'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 司机特有字段
    car_model = db.Column(db.String(100))
    plate_number = db.Column(db.String(20))
    rating = db.Column(db.Float, default=5.0)
    completed_trips = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'user_type': self.user_type,
            'car_model': self.car_model,
            'plate_number': self.plate_number,
            'rating': self.rating,
            'completed_trips': self.completed_trips
        }


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_point = db.Column(db.String(200), nullable=False)
    end_point = db.Column(db.String(200), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'ongoing', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    driver = db.relationship('User', backref='driver_trips')

    def to_dict(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'departure_time': self.departure_time.strftime('%Y-%m-%d %H:%M'),
            'available_seats': self.available_seats,
            'price': self.price,
            'status': self.status,
            'driver': {
                'name': self.driver.name,
                'car_model': self.driver.car_model,
                'plate_number': self.driver.plate_number,
                'rating': self.driver.rating
            }
        }


class RideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_point = db.Column(db.String(200), nullable=False)
    end_point = db.Column(db.String(200), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # 'active', 'matched', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    passenger = db.relationship('User', backref='ride_requests')

    def to_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'passenger_name': self.passenger.name,
            'start_point': self.start_point,
            'end_point': self.end_point,
            'departure_time': self.departure_time.strftime('%Y-%m-%d %H:%M'),
            'seats': self.seats,
            'note': self.note,
            'status': self.status
        }


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # 'confirmed', 'completed', 'cancelled'
    paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    trip = db.relationship('Trip', backref='bookings')
    passenger = db.relationship('User', backref='passenger_bookings')

    def to_dict(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'passenger_id': self.passenger_id,
            'seats': self.seats,
            'amount': self.amount,
            'status': self.status,
            'paid': self.paid,
            'trip': self.trip.to_dict(),
            'passenger': self.passenger.to_dict()
        }


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'sender': self.sender.to_dict()
        }