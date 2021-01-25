from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Doctors, Patient, Appointment, Hospital, Department
from wtforms.fields.html5 import DateTimeLocalField
import phonenumbers



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_phone(self, phone):

        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()

        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class RegistrationDepartmentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    hospital = SelectField(u'Hospital', coerce=int)

    name = StringField('Department name', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



class AddHospitalForm(FlaskForm):
    name = StringField('Hospital name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    submit = SubmitField('Add Hospital')

class AddDoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Register')

    
class DateForm(FlaskForm):
    startdate = DateTimeLocalField("date", validators=[DataRequired()])
    submit = SubmitField('Submit')

class BookForm(FlaskForm):
    startdate = DateTimeLocalField("date")
    submit = SubmitField('Submit')

class CancelForm(FlaskForm):
    id = IntegerField("Id Number of Appointment to Cancel: ")
    submit = SubmitField("Cancel appointment")

class BookInternalForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    firstname = StringField('First name', validators=[DataRequired()])
    lastname = StringField('Last name', validators=[DataRequired()])
    apdate = DateField("Date")
    aptime = SelectField('Time', validators=[DataRequired()])
    doctor = SelectField(u'Doctor', coerce=int)
    location = SelectField(u'Location', coerce=int)
    submit = SubmitField("Submit appointment")

class AddWorkingTimeForm(FlaskForm):
    doctor = SelectField(u'Doctor', coerce=int)
    startdate = DateField("Start Date", validators=[DataRequired()])
    enddate = DateField("End Date", validators=[DataRequired()])
    starttime = StringField('Start Time', validators=[DataRequired()])
    endtime = StringField('End Time', validators=[DataRequired()])
    submit = SubmitField("Submit working time")

    def validate_date(self, enddate, startdate):                                                         
        if enddate.data < startdate.data:                                          
            raise ValidationError('Please check the dates again')

class AddLocationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    adress = StringField('Adress', validators=[DataRequired()])
    room = StringField('Room / Floor / Buildingnumber', validators=[DataRequired()])
    colortape = StringField('Colortape', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField("Submit")

class BookPatientForm(FlaskForm):
    city = SelectField(u'City')
    department = SelectField(u'Department')
    hospital = SelectField(u'Hospital', coerce=int)
    apdate = DateField("Date")
    aptime = SelectField('Time', validators=[DataRequired()])
    submit = SubmitField("Submit appointment")
