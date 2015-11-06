from flask import Flask
from flask.ext.cas import CAS

application = Flask(__name__)
application.config.from_object('config')
application.config['CAS_SERVER'] = 'https://sso.acu.edu' 
application.config['CAS_AFTER_LOGIN'] = 'route_home'
CAS(application)

from app import views