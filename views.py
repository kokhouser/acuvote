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

# @application.route("/")
# @login_required
# def route_home():
# 	return redirect(url_for('vote_page'))

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

@application.route("/elections/")
@application.route("/elections/<electionid>")
def vote_page(electionid=None):
	cur = g.db.execute('select distinct position from candidates where electionid = (?)', [electionid])
	positions = [dict(name=row[0]) for row in cur.fetchall()]
	elections = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
	# for i in positions:
	# 	cur = g.db.execute('select * from voted where electionid=(?) and username=(?)', [i['id'], 'jrn11a'])
	# 	if len(cur.fetchall())==0:
	# 		i['voted'] = False;
	# 	else:
	# 		i['voted'] = True;
	candidates = []
	for i in positions:
		print i
		cur = g.db.execute('select * from candidates inner join voters on candidates.voterid = voters.id where candidates.electionid = (?) and candidates.position = (?)', [electionid,i['name']])
		category_candidates = [dict(id=row[0], fname=row[6], lname=row[7], voterid=row[2],votes=row[4]) for row in cur.fetchall()]	
		candidates.append(category_candidates)

	# cur = g.db.execute('select * from candidates')
	# candidates = [dict(id=row[0], electionid=row[1], voterid=row[2], votes=row[4]) for row in cur.fetchall()]	
	# for i in candidates:
	# 	cur = g.db.execute('select fname, lname from voters where id=(?)', [i['voterid']])
	# 	fetched = [dict(firstname=row[0],lastname=row[1]) for row in cur.fetchall()]
	# 	i['fname'] = fetched[0]['firstname']
	# 	i['lname'] = fetched[0]['lastname']
	print candidates
	return render_template("body.html", positions=positions, candidates=candidates)
	#return render_template("body.html")

@application.route("/google")
def google_page():
	return render_template("google.html")

@application.route("/vote", methods=['GET', 'POST'])
def cast_vote():
	if request.method=='POST':
		something = dict(request.form)
		eid = 0
		username = 0
		for key,value in something.iteritems():
			cur2 = g.db.execute('select votes from candidates where electionid=(?) and voterid=(?)', [key, something[key][0]] )
			fetched = [dict(votes=row[0]) for row in cur2.fetchall()]
			num_votes = fetched[0]['votes']+1
			g.db.execute('update candidates set votes=(?) where electionid=(?) and voterid=(?)', [num_votes, key, something[key][0]])
			g.db.commit()

		g.db.execute('insert into voted (electionid, username) values ((?), (?))', [eid, 'jrn11a'])
		g.db.commit()
		return redirect(url_for('vote_page'))

# @application.route("/populate")
# def populate():


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	application.run(debug=True, host='0.0.0.0')







	