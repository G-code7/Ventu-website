from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy.orm import validates
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="active", nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    phone = db.Column(db.String(50), nullable=True)
    
    # Relaciones mejoradas con parámetros explícitos
    provider = db.relationship('Provider', back_populates='user', uselist=False, cascade='all, delete-orphan')
    client = db.relationship('Client', back_populates='user', uselist=False, cascade='all, delete-orphan')

    @validates('role')
    def validate_role(self, key, value):
        if value not in ['provider', 'client']:
            raise ValueError(f"Rol inválido: {value}")
        return value

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "phone": self.phone
        }

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User', back_populates='client')
    favorites = db.relationship('FavoriteTourPlan', back_populates='client', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat()
        }

class Provider(db.Model):
    __tablename__ = 'provider'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = db.relationship('User', back_populates='provider')
    tour_plans = db.relationship('TourPlan', back_populates='provider', cascade='all, delete-orphan')

class TourPlan(db.Model):
    __tablename__ = 'tour_plan'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    provider = db.relationship('Provider', back_populates='tour_plans')
    favorites = db.relationship('FavoriteTourPlan', back_populates='tour_plan', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "available_spots": self.available_spots,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "provider_id": self.provider_id,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat()
        }

class ReservationStatus(Enum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    reservation_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = db.Column(SQLAlchemyEnum(ReservationStatus), default=ReservationStatus.ACTIVE)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    tour_plan_id = db.Column(db.Integer, db.ForeignKey('tour_plan.id'), nullable=False)

    client = db.relationship('Client', backref='reservations')
    tour_plan = db.relationship('TourPlan', backref='reservations')

    def serialize(self):
        return {
            'id': self.id,
            'reservation_date': self.reservation_date.isoformat(),
            'status': self.status.value,
            'client_id': self.client_id,
            'tour_plan_id': self.tour_plan_id
        }

class FavoriteTourPlan(db.Model):
    __tablename__ = 'favorite_tour_plan'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    tour_plan_id = db.Column(db.Integer, db.ForeignKey('tour_plan.id'), nullable=False)

    client = db.relationship('Client', back_populates='favorites')
    tour_plan = db.relationship('TourPlan', back_populates='favorites')

    def serialize(self):
        return self.tour_plan.serialize()