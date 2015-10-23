from flask import Flask
from flask.ext.cas import CAS

app = Flask(__name__)
app.config.from_object('config')
app.config['CAS_SERVER'] = 'https://sso.acu.edu' 
app.config['CAS_AFTER_LOGIN'] = 'route_home'
CAS(app)

from app import views