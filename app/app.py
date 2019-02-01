import os,sys

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from helpers.apparse import AppSettings


app = Flask(__name__, template_folder="templates")
[AppSettings.loadEnvironment(app_file) for app_file in sys.argv[1:]]
app.secret_key = os.environ["DARK_STAR_WOMBAT"]
print("I am in app: %s" % type(app))
#handlers.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MODE = 'dev'
db = SQLAlchemy(app)

try:
    db.session.execute('SELECT 1')
    print("got a result from simple query of SELECT 1 ...")
except Exception as ex:
    print("problem with db.execute", ex)






