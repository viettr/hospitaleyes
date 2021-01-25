from flask import render_template, flash, redirect, url_for, request, json, make_response, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, DateForm, CancelForm, BookForm, AddDoctorForm, AddHospitalForm, RegistrationDepartmentForm, BookInternalForm, AddWorkingTimeForm, AddLocationForm, BookPatientForm
from app.models import User, Appointment, Doctors, Patient, Hospital, Department, DoctorDate, TimeSlots, Location
from datetime import datetime
import pandas as pd
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

send_message = True

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # redirect already logged in user to their home screen
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # load the form
    form = LoginForm()
    if form.validate_on_submit():
        # add user to database
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # log user in
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
    # only allow for already added hospitals
    form.hospital.choices = [(g.id, g.name) for g in Hospital.query.order_by('name')]
    # if department has not been registered add to database
    if form.validate_on_submit():
        if Department.query.filter_by(name=form.name.data, hospital_id=form.hospital.data).first() is None:
            hospital_dep = Hospital.query.filter_by(id=form.hospital.data).first()
            department = Department(name=form.name.data, hospital=hospital_dep)
            db.session.add(department)
        # connect user to department
        department = Department.query.filter_by(name=form.name.data, hospital_id=form.hospital.data).first()
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
            times = (pd.DataFrame(columns=['NULL'],
            index=pd.date_range('2016-09-02T07:00:00Z', '2016-09-02T18:00:00Z',
            freq='15T'))
            .index.strftime('%H:%M')
            .tolist())

            form = BookInternalForm()
            form.doctor.choices = [
                (g.id, g.name) for g in Doctors.query.filter_by(department_id = current_user.department_id).order_by('name')]
            form.aptime.choices = [(g, g) for g in times]
            locations = Location.query.filter_by(department_id = current_user.department_id).order_by('name')
            if locations.first() is None:
                form.location.choices = []
            else:
                form.location.choices = [(g.id, g.name) for g in locations]

            if form.validate_on_submit():
                if Patient.query.filter_by(phone=form.phone.data).first() is None:
                    patient = Patient(phone=form.phone.data)
                    db.session.add(patient)

                patient = Patient.query.filter_by(phone=form.phone.data).first()
                doc = Doctors.query.filter_by(id=form.doctor.data).first()
                appoint = Appointment(apdate=str(form.apdate.data), aptime=str(form.aptime.data), patient=patient, doctor=doc)
                db.session.add(appoint)
                db.session.commit()


                if send_message:
                    location=Location.query.filter_by(id = form.location.data).first()
                    text_start = "Thank you for your appointment with " + doc.name + " at " + str(form.apdate.data) + " " + form.aptime.data + ". "
                    text_adress = " Come to " + location.adress + " to the room " + location.room + " by following the color " + location.colortape + ". You can find the map " + location.link + ". " 
                    text_process = "Bring your isurance card."
                    text_body = text_start + text_adress + text_process
                    message = client.messages.create(
                    to=form.phone.data,
                    from_='HSPTLEYES',
                    body=text_body)



                flash('The appointment has been made')
                return redirect(url_for('book_internal_appointment'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    return render_template('book_internal_appointment.html', title='Appointment', form=form)



@app.route('/_update_timeslots', methods=['GET', 'POST'])
def update_timeslots():
    times = []
    startdate = request.args.get('date')
    doctor = request.args.get('doc')
    doctor_id = doctor
    date = DoctorDate.query.filter_by(date=startdate, doctor_id=doctor_id).first()
    if date is None:
        times = []
    else:
        times = TimeSlots.query.filter_by(doctor_date_id = date.id).all()
        times = [t.slot for t in times]
    Aptimes = Appointment.query.filter_by(apdate=startdate, doctor_id = doctor_id).all()
    if not Aptimes is None:
        Time = [aptime.aptime for aptime in Aptimes]
        times = [x for x in times if x not in Time]

    response = make_response(json.dumps(times))
    response.content_type = 'application/json'
    return response

@app.route('/myappointments', methods=['GET', 'POST'])
@login_required
def myappointments():
    appointments = db.session.query(Appointment).outerjoin(Doctors).outerjoin(Department).filter(Appointment.patient_id ==  current_user.patient_id).all()
    table_header = ["#", "Date", "Time", "Doctor"]
    appoint = []
    for appoin in appointments:
        appoint.append([appoin.id, appoin.apdate, appoin.aptime, appoin.doctor.name])

    return render_template('myappointments.html', title='Appointment', table_header=table_header, appointments= appoint)

@app.route('/add_workingtime', methods=['GET', 'POST'])
@login_required
def add_workingtime():
    form = AddWorkingTimeForm()
    form.doctor.choices = [
    (g.id, g.name) for g in Doctors.query.filter_by(department_id = current_user.department_id).order_by('name')]            
    if form.validate_on_submit():
        daterange = pd.date_range(start=form.startdate.data, end=form.enddate.data)
        daterange = [d.strftime('%Y-%m-%d') for d in daterange]
        doctor = Doctors.query.filter_by(id=form.doctor.data).first()
        times = (pd.DataFrame(columns=['NULL'],
        index=pd.date_range('2016-09-02T07:00:00Z', '2016-09-02T18:00:00Z',
        freq='15T'))
        .between_time(form.starttime.data,form.endtime.data)
        .index.strftime('%H:%M')
        .tolist())
        for i in daterange:
            date = DoctorDate(date=i, doctor=doctor)
            db.session.add(date)
            db.session.commit()
            date = DoctorDate.query.filter_by(date=i, doctor_id=doctor.id).first()
            for j in times:
                time = TimeSlots(slot = j, date = date)
                db.session.add(time)
                db.session.commit()

    return render_template('add_workingtime.html', title='Appointment', form=form)

@app.route('/add_location', methods=['GET', 'POST'])
@login_required
def add_location():
    form = AddLocationForm()
    if form.validate_on_submit():
        department = Department.query.filter_by(id = current_user.department_id).first()
        location = Location(name=form.name.data, adress = form.adress.data, room = form.room.data, colortape=form.colortape.data, link=form.link.data, department = department)
        db.session.add(location)
        db.session.commit()
        flash('The location has been added!')
    return render_template('add_location.html', form=form)   

@app.route('/book_appointment_patient', methods=['GET', 'POST'])
@login_required
def book_appointment_patient():
    form = BookPatientForm()
    city_choices = Hospital.query.with_entities(Hospital.city).distinct().all()
    city_choices = [h[0] for h in city_choices]
    form.city.choices = city_choices
    department_choices = Department.query.with_entities(Department.name).distinct().all()
    department_choices = [d[0] for d in department_choices]
    form.department.choices = department_choices
    hospital_choices = Hospital.query.with_entities(Hospital.id).distinct().all()
    hospital_choices = [h[0] for h in hospital_choices]
    form.hospital.choices = hospital_choices
    times = (pd.DataFrame(columns=['NULL'],
    index=pd.date_range('2016-09-02T00:00:00Z', '2016-09-02T23:55:00Z',
    freq='15T')).between_time("00:00","23:55").index.strftime('%H:%M').tolist())
    form.aptime.choices = times
    if form.validate_on_submit():
        patient = Patient.query.filter_by(phone=current_user.patient_id).first()
        doc_match = db.session.query(TimeSlots).outerjoin(DoctorDate).outerjoin(Doctors).outerjoin(Department).outerjoin(Hospital).filter(Hospital.id ==  form.hospital.data, Department.name == form.department.data, DoctorDate.date == form.apdate.data, TimeSlots.slot == form.apdate.data).with_entities(DoctorDate.doctor_id).all()
        Aptimes = db.session.query(Appointment).outerjoin(Doctors).outerjoin(Department).outerjoin(Hospital).filter(Hospital.id ==  form.hospital.data, Department.name == form.department.data, DoctorDate.date == form.apdate.data, Appointment.aptime == form.aptime.data).with_entities(Appointment.doctor_id).all()            
        if not Aptimes is None:
            doc_match = [x for x in doc_match if x not in Aptimes]        
        doc_match = [t[0] for t in doc_match]
        doc = Doctors.query.filter_by(id=doc_match).first()
        appoint = Appointment(apdate=str(form.apdate.data), aptime=str(form.aptime.data), patient=patient, doctor=doc)
        db.session.add(appoint)
        db.session.commit()
        if send_message:
            location=Location.query.filter_by(id = doc.department_id).first()
            text_start = "Thank you for your appointment with " + doc.name + " at " + str(form.apdate.data) + " " + form.aptime.data + ". "
            text_adress = " Come to " + location.adress + " to the room " + location.room + " by following the color " + location.colortape + ". You can find the map " + location.link + ". " 
            text_process = "Bring your isurance card."
            text_body = text_start + text_adress + text_process
            message = client.messages.create(
            to=patient.phone,
            from_='HSPTLEYES',
            body=text_body)

        flash('Your appointment has been made!')
    return render_template('book_appointment_patient.html', form=form)   

@app.route('/_update_hospital', methods=['GET', 'POST'])
def update_hospital():
    city = request.args.get('city')
    department = request.args.get('department')
    hospitals = db.session.query(Hospital, db.func.count(TimeSlots.id)).outerjoin(Department).outerjoin(Doctors).outerjoin(DoctorDate).outerjoin(TimeSlots).filter(Hospital.city ==  city, Department.name == department).group_by(Hospital.name).all()
    if hospitals is None:
        hospitals = []
    else:
        hospitals = [(t[0].id, t[0].name + " Available Slots: " + str(t[1])) for t in hospitals]

    response = make_response(json.dumps(hospitals))
    response.content_type = 'application/json'
    return response

@app.route('/_update_timeslots_patient', methods=['GET', 'POST'])
def update_timeslots_patient():
    department = request.args.get('department')
    hospital = request.args.get('hospital')
    date = request.args.get('date')
    timeslots = db.session.query(TimeSlots).outerjoin(DoctorDate).outerjoin(Doctors).outerjoin(Department).outerjoin(Hospital).filter(Hospital.id ==  hospital, Department.name == department, DoctorDate.date == date).with_entities(TimeSlots.slot, DoctorDate.doctor_id).all()
    if timeslots is None:
        timeslots = []
    else:
        Aptimes = db.session.query(Appointment).outerjoin(Doctors).outerjoin(Department).outerjoin(Hospital).filter(Hospital.id ==  hospital, Department.name == department, DoctorDate.date == date).with_entities(Appointment.aptime, Appointment.doctor_id).all()            
        if not Aptimes is None:
            timeslots = [x for x in timeslots if x not in Aptimes]
        timeslots = [t[0] for t in timeslots]
        timeslots = list(set(timeslots))
        timeslots.sort()
    response = make_response(json.dumps(timeslots))
    response.content_type = 'application/json'
    return response