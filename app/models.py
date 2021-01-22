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

    def __repr__(self):
        return f"Hospital {self.name} from {self.city}"


class Department(db.Model):
    __tablename__ = 'Department'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    hospital = db.Column(db.String(120))
    users = db.relationship('User', backref='department', lazy='dynamic')
    doctors = db.relationship('Doctors', backref='department', lazy='dynamic')


class Doctors(db.Model):
    __tablename__ = 'Doctors'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('Department.id'))
    appointment = db.relationship('Appointment',backref='doctor',lazy='dynamic')

    def __repr__(self):
        return f"Doctor {self.name} from {self.department_id} department"

class Patient(db.Model):

    __tablename__ = 'Patient'

    id = db.Column(db.Integer, primary_key = True)    
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

class SMStext(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    confirmation_SMS = db.Column(db.Text)
    status_SMS = db.Column(db.Text)
    Cancel_SMS = db.Column(db.Text)
    doctor_id = db.Column(db.Integer,db.ForeignKey('Doctors.id'))

    def __init__(self,confirmation_SMS,Status_SMS,Cancel_SMS,doctor_id):
        self.confirmation_SMS = confirmation_SMS
        self.status_SMS = Status_SMS
        self.Cancel_SMS = Cancel_SMS
        self.doctor_id = doctor_id
    
    def __repr__(self):
        return f"{self.confirmation_SMS},{self.Cancel_SMS},{self.doctor_id}"
