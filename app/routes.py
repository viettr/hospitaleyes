from flask import render_template, flash, redirect, url_for, request, json, make_response, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, DateForm, CancelForm, BookForm, AddDoctorForm, AddHospitalForm, RegistrationDepartmentForm, BookInternalForm, BookInternalTestForm
from app.models import User, Appointment, Doctors, SMStext, Patient, Hospital, Department
from datetime import datetime
import pandas as pd



@app.route('/')
def home():
    return render_template("home.html")
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('register.html', title='Register')

@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():

        if Patient.query.filter_by(phone=form.phone.data).first() is None:
            patient = Patient(phone=form.phone.data)
            db.session.add(patient)

        patient = Patient.query.filter_by(phone=form.phone.data).first()
        user = User(username=form.username.data, email=form.email.data, role="patient", patient = patient)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered patient!')
        return redirect(url_for('login'))
    return render_template('register_patient.html', title='Register', form=form)


@app.route('/register_department', methods=['GET', 'POST'])
def register_department():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationDepartmentForm()
    form.hospital.choices = [g.name for g in Hospital.query.order_by('name')]

    if form.validate_on_submit():
        if Department.query.filter_by(name=form.name.data, hospital=form.hospital.data).first() is None:
            department = Department(name=form.name.data, hospital=form.hospital.data)
            db.session.add(department)

        department = Department.query.filter_by(name=form.name.data, hospital=form.hospital.data).first()
        user = User(username=form.username.data, email=form.email.data, role="hospital", department = department)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered department!')
        return redirect(url_for('login'))
    return render_template('register_department.html', title='Register', form=form)



@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    form = AddHospitalForm()
    if form.validate_on_submit():
        hospital = Hospital(name=form.name.data, city=form.city.data)
        db.session.add(hospital)
        db.session.commit()
        flash('The hospital has been added!')
    return render_template('add_hospital.html', form=form)    

@app.route('/adddoctor', methods=['GET', 'POST'])
def add_doctor():
    if current_user.is_authenticated:
        if current_user.role == "hospital":
            form = AddDoctorForm()
            if form.validate_on_submit():
                dep = Department.query.filter_by(id = current_user.department_id).first()               
                doc = Doctors(name=form.name.data, department=dep)
                db.session.add(doc)
                db.session.commit()
                flash('New Doctor added!')
                return redirect(url_for('index'))
            return render_template('add_doctor.html', title='Add doctor', form=form)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/date', methods=['GET','POST'])
def date():
    return render_template('date.html', title='Date')

@app.route('/addDate', methods=['GET','POST'])
def addDate():
    if request.method == "POST":
        startdate = request.form.get("basicDate")
    return startdate



@app.route('/list')
def appointment_list():

    appointment_list = Appointment.query.filter_by(patient_id == current_user.id).all()
    return render_template('list.html',list = appointment_list)

@app.route('/Cancel',methods=['GET','POST'])
def cancel_appointmetn():

    form = CancelForm()

    if form.validate_on_submit():

        id = form.id.data
        ap = Appointment.query.det(id)
        db.session.delete(ap)
        db.session.commmit()

        return redirect(url_for('list.html'))


@app.route('/book_internal_appointment', methods=['GET', 'POST'])
def book_internal_appointment():
    if current_user.is_authenticated:
        if current_user.role == "hospital":
            form = BookInternalForm()
            form.doctor.choices = [
                (g.id, g.name) for g in Doctors.query.filter_by(department_id = current_user.department_id).order_by('name')]

            if form.validate_on_submit():
                if Patient.query.filter_by(phone=form.phone.data).first() is None:
                    patient = Patient(phone=form.phone.data)
                    db.session.add(patient)

                patient = Patient.query.filter_by(phone=form.phone.data).first()
                doc = Doctors.query.filter_by(id=form.doctor.data).first()
                appoint = Appointment(apdate=form.apdate.data, aptime=form.aptime.data, patient_id=patient, doctor_id=doc)
                db.session.add(appoint)
                db.session.commit()
                flash('The appointment has been made')
                return redirect(url_for('/'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return render_template('book_internal_appointment.html', title='Appointment', form=form)


@app.route('/book_internal_appointment_test', methods=['GET', 'POST'])
def book_internal_appointment_test():
    if current_user.is_authenticated:
        if current_user.role == "hospital":
            times = (pd.DataFrame(columns=['NULL'],
            index=pd.date_range('2016-09-02T07:00:00Z', '2016-09-02T18:00:00Z',
            freq='15T'))
            .index.strftime('%H:%M')
            .tolist())

            form = BookInternalTestForm()
            form.doctor.choices = [
                (g.id, g.name) for g in Doctors.query.filter_by(department_id = current_user.department_id).order_by('name')]
            form.aptime.choices = [(g, g) for g in times]

            if form.validate_on_submit():
                if Patient.query.filter_by(phone=form.phone.data).first() is None:
                    patient = Patient(phone=form.phone.data)
                    db.session.add(patient)

                patient = Patient.query.filter_by(phone=form.phone.data).first()
                doc = Doctors.query.filter_by(id=form.doctor.data).first()
                appoint = Appointment(apdate=str(form.apdate.data), aptime=str(form.aptime.data), patient=patient, doctor=doc)
                db.session.add(appoint)
                db.session.commit()
                flash('The appointment has been made')
                return redirect(url_for('book_internal_appointment_test'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return render_template('book_internal_appointment_test.html', title='Appointment', form=form)


@app.route('/_update_timeslots', methods=['GET', 'POST'])
def update_timeslots():
    times = []
    startdate = request.args.get('date')
    doctor = request.args.get('doc')
    doctor_id = doctor
    times = (pd.DataFrame(columns=['NULL'],
    index=pd.date_range('2016-09-02T07:00:00Z', '2016-09-02T18:00:00Z',
    freq='15T'))
    .between_time('07:00','21:00')
    .index.strftime('%H:%M')
    .tolist())
    Aptimes = Appointment.query.filter_by(apdate=startdate, doctor_id = doctor_id).all()
    if not Aptimes is None:
        Time = [aptime.aptime for aptime in Aptimes]
        times = [x for x in times if x not in Time]

    response = make_response(json.dumps(times))
    response.content_type = 'application/json'
    return response

