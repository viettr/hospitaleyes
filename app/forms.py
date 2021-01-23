from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Doctors, Patient, Appointment, SMStext, Hospital, Department
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
        user = Patient.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Please use a different phone.')

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
    hospital = SelectField(u'Hospital')

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
    apdate = DateField("date")
    aptime = SelectField('Time', validators=[DataRequired()])
    doctor = SelectField(u'Doctor', coerce=int)
    submit = SubmitField("Submit appointment")