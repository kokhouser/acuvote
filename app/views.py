import sqlite3
from flask import Flask, g, render_template, flash, redirect, session, url_for, request, abort
from app import application
from flask.ext.cas import CAS
from flask.ext.cas import login_required
from contextlib import closing

DATABASE = '/tmp/vote.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# @application.route("/")
# @login_required
# def route_home():
# 	return (cas.username)

@application.route("/vote")
def vote_page():
	elections = range(0,10)
	candidates = range(0,10)
	return render_template("body.html", elections=elections, candidates=candidates)

@application.route("/google")
def google_page():
	return render_template("google.html")

# @application.route("/populate")
# def populate():


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def connect_db():
    return sqlite3.connect(application.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with application.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# @application.before_request
# def before_request():
# 	g.db = connect_db()

# @application.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()



	