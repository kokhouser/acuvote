import sqlite3
from flask import Flask, g, render_template, flash, redirect, session, url_for, request, abort
from app import application
from flask.ext.cas import CAS
from flask.ext.cas import login_required
from contextlib import closing

DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# @application.route("/")
# @login_required
# def route_home():
# 	return (cas.username)
def connect_db():
	return sqlite3.connect('/tmp/test.db')

def init_db():
	print 'here'
	with closing(connect_db()) as db:
		with application.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		print 'here'
		db.commit()

@application.before_request
def before_request():
	g.db = connect_db()

@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@application.route("/vote")
def vote_page():
	cur = g.db.execute('select * from elections')
	elections = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
	cur = g.db.execute('select * from candidates')
	candidates = [dict(electionid=row[1], voterid=row[2]) for row in cur.fetchall()]
	for i in candidates:
		cur = g.db.execute('select fname, lname from voters where id=%s' % i['voterid'])
		fetched = [dict(firstname=row[0],lastname=row[1]) for row in cur.fetchall()]
		i['fname'] = fetched[0]['firstname']
		i['lname'] = fetched[0]['lastname']
	return render_template("body.html", elections=elections, candidates=candidates)
	#return render_template("body.html")

@application.route("/google")
def google_page():
	return render_template("google.html")

# @application.route("/populate")
# def populate():


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'







	