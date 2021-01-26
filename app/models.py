from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('Department.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'))

    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Hospital(db.Model):
    __tablename__ = 'Hospital'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    department = db.relationship('Department', backref='hospital', lazy='dynamic')

    def __repr__(self):
        return f"Hospital {self.name} from {self.city}"


class Department(db.Model):
    __tablename__ = 'Department'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    users = db.relationship('User', backref='department', lazy='dynamic')
    doctors = db.relationship('Doctors', backref='department', lazy='dynamic')
    location = db.relationship('Location', backref='department', lazy='dynamic')
    hospital_id = db.Column(db.Integer, db.ForeignKey('Hospital.id'))

class Location(db.Model):
    __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    adress = db.Column(db.String(120))
    room = db.Column(db.String(120))
    colortape = db.Column(db.String(120))
    link = db.Column(db.String(120))
    department_id = db.Column(db.Integer, db.ForeignKey('Department.id'))

class Doctors(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('Department.id'))
    docdate = db.relationship('DoctorDate',backref='doctor',lazy='dynamic')
    appointment = db.relationship('Appointment',backref='doctor',lazy='dynamic')

    def __repr__(self):
        return f"Doctor {self.name} from {self.department_id} department"

class DoctorDate(db.Model):
    __tablename__ = 'DoctorDate'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(80))
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.id'))
    timeslots = db.relationship('TimeSlots',backref='date',lazy='dynamic')

class TimeSlots(db.Model):
    __tablename__ = 'TimeSlots'
    id = db.Column(db.Integer, primary_key = True)
    slot = db.Column(db.String(80))
    free = db.Column(db.String(80))
    doctor_date_id = db.Column(db.Integer, db.ForeignKey('DoctorDate.id'))


class Patient(db.Model):

    __tablename__ = 'Patient'

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(120))        
    lastname = db.Column(db.String(120))    
    phone = db.Column(db.String(120),index=True, unique=True)
    users = db.relationship('User', backref='patient', lazy='dynamic')
    appointment = db.relationship('Appointment',backref='patient',lazy='dynamic')

class Appointment(db.Model):

    __tablename__ = 'Appointment'

    id = db.Column(db.Integer, primary_key = True)
    apdate = db.Column(db.String, nullable=False)
    aptime = db.Column(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('Doctors.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('Patient.id'))

    def __init__(self, apdate, aptime, **kwargs):
        super(Appointment, self).__init__(**kwargs)
        self.apdate = apdate
        self.aptime = aptime
    
    def __repr__(self):
        return f"Appointment {self.apdate}"