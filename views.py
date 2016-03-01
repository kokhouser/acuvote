import sqlite3
import flask
from flask import Flask, g, render_template, flash, redirect, session, url_for, request, abort
from flask.ext.cas import CAS
from flask.ext.cas import login_required
from contextlib import closing

cas = CAS()
application = Flask(__name__)
cas.init_app(application)
application.config['CAS_SERVER'] = 'https://sso.acu.edu' 
application.config['CAS_AFTER_LOGIN'] = 'route_home'
application.config['CAS_VALIDATE_ROUTE'] = '/serviceValidate'
application.debug = True
DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

@application.route("/")
@login_required
def route_home():
	return redirect(url_for('vote_page'))

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

@application.route("/elections")
def vote_page():
	cur = g.db.execute('select * from elections')
	elections = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
	cur = g.db.execute('select * from candidates')
	candidates = [dict(id=row[0], electionid=row[1], voterid=row[2], votes=row[4]) for row in cur.fetchall()]
	for i in candidates:
		cur = g.db.execute('select fname, lname from voters where id=(?)', [i['voterid']])
		fetched = [dict(firstname=row[0],lastname=row[1]) for row in cur.fetchall()]
		i['fname'] = fetched[0]['firstname']
		i['lname'] = fetched[0]['lastname']
	return render_template("body.html", elections=elections, candidates=candidates)
	#return render_template("body.html")

@application.route("/google")
def google_page():
	return render_template("google.html")

@application.route("/vote", methods=['GET', 'POST'])
def cast_vote():
	print "QWQEWEE"
	if request.method=='POST':
		something = dict(request.form)
		print "THIS IS SOMETHING", something
		for key,value in something.iteritems():
			print "THIS IS THE KEY", key
			print "THIS IS THE VALUE", something[key][0]
			cur2 = g.db.execute('select votes from candidates where electionid=(?) and voterid=(?)', [key, something[key][0]] )
			fetched = [dict(votes=row[0]) for row in cur2.fetchall()]
			print "THIS IS FETCHED", fetched
			num_votes = fetched[0]['votes']+1
			print "THIS IS NUM VOTES", num_votes
			g.db.execute('update candidates set votes=(?) where electionid=(?) and voterid=(?)', [num_votes, key, something[key][0]])
			g.db.commit()
		return redirect(url_for('vote_page'))

# @application.route("/populate")
# def populate():


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	application.run(debug=True)







	
