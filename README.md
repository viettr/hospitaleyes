# hospitaleyes

This is the repository for a university project. The homepage can be used locally or deployed on heroku. The homepage uses mainly python with flask to show the pages. The data is stored in a database (app.db). The files "Procfile" and "runtime.txt" are only needed if you want to deploy the website on heroku. The web app has two main views: one for the patient and one for the hospitals (especally the departments of a hospital). The patients can book an appointment and see their appointments. The departments can add doctors, add working time for the doctors, add a description how to reach their department and book an internal appointment for their own department. 


Installation locally
==============================
We assume that python 3 is installed. The following line of code should be executed in the terminal

1. download the folder: `git clone https://github.com/viettr/hospitaleyes.git`
2. move into the folder: `cd hospitaleyes`
3. optional create a virtual environment: `python3 -m venv venv` then `source venv/bin/activate` (or on windows `venv\Scripts\activate`)
4. install the dependencies: `pip3 install -r requirements.txt`
5. set the path to the app: `export FLASK_APP=<PATH of hospital.py>` (or `set` in windows)
6. run the app: `flask run`

go the the browser and type in: http://127.0.0.1:5000/ to see the webpage.

Installation heroku
==============================
Assumption: have heroku account

1. get heroku cli from: https://devcenter.heroku.com/articles/heroku-cli
2. login: `heroku login`
3. download the folder: `git clone https://github.com/viettr/hospitaleyes.git`
4. move into the folder: `cd hospitaleyes`
5. create a heroku app: `heroku apps:create <app name>`
6. add a database: `heroku addons:add heroku-postgresql:hobby-dev`
7. define the flask app: `heroku config:set FLASK_APP=hospital.py`
8. push to heroku `git checkout -b deploy` and then `git push heroku deploy:master` then `git commit -a -m "heroku deployment changes"` then `git push heroku master`

Further information: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku

Code Organization
------------

    ├── app                     <- Stored code
    │   ├── templates           <- Stored html files
    │   ├── __init__.py         <- Initiate the app
    │   ├── errors.py           <- Generate error pages
    │   ├── forms.py            <- Initiate the forms
    │   └── models.py           <- Define databank structure
    │   └── routes.py           <- This is where the app redirects to the
    ├── migrations              <- Migrate (update) database
    ├── .gitignore              
    ├── app.db                  <- The database
    ├── config.py               <- Stored configurations
    ├── hospital.py             <- Inititate file on top level
    ├── Procfile                <- Configure heroku settings
    ├── README.md               <- The top-level README for developers using this projec
    ├── rquirements.txt         <- The requirements file to automatically install all dependencies
    ├── runtime.txt             <- Define the python version for heroku