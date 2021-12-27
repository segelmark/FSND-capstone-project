from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


'''
Therapist
'''
class Therapist(db.Model):  
  __tablename__ = 'Therapist'

  id = Column(db.Integer, primary_key=True)
  name = Column(db.String)
  bookings = db.relationship('Booking', backref='therapist', lazy=True, cascade="all, delete")

  def __init__(self, name):
    self.name = name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }

'''
Bookings
'''
class Booking(db.Model):  
  __tablename__ = 'Booking'

  id = Column(db.Integer, primary_key=True)
  therapist_id = db.Column(db.Integer, db.ForeignKey('Therapist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


  def format(self):
    return {
      'id': self.id,
      'therapist_id': self.therapist_id,
      'start_time': self.start_time
      }