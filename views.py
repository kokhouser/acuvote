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
#	session['username'] = cas.username
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
	# if not cas.username:
	# 	return redirect(url_for(route_home))
	cur = g.db.execute('select id from elections where id = (?)', [electionid])
	if electionid and len(cur.fetchall()) == 0:
		return render_template('body.html', error="Sorry that election does not exist. Here are some that might though.")
	if electionid:
		cur = g.db.execute('select * from voted where username=(?) and electionid=(?)', [cas.username,electionid])
		if len(cur.fetchall()) > 0:
			return render_template("body.html", error="Sorry, you have already voted for this election")
		cur = g.db.execute('select * from elections where id = (?)', [electionid])
		electionname = [dict(name=row[1]) for row in cur.fetchall()][0]['name']
		cur = g.db.execute('select distinct position from candidates where electionid = (?)', [electionid])
		positions = [dict(name=row[0]) for row in cur.fetchall()]
		candidates = []
		for i in positions:
			print i
			cur = g.db.execute('select * from candidates inner join voters on candidates.voterid = voters.id where candidates.electionid = (?) and candidates.position = (?)', [electionid,i['name']])
			category_candidates = [dict(id=row[0], fname=row[6], lname=row[7], voterid=row[2],votes=row[4]) for row in cur.fetchall()]	
			candidates.append(category_candidates)

		print candidates
		return render_template("body.html", electionname=electionname, electionid=electionid, positions=positions, candidates=candidates)
	else:
		cur = g.db.execute('select * from elections')
		elections = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

		return render_template("body.html", elections=elections, thankyou=request.args.get('thankyou'), error=request.args.get('error'))

@application.route("/google")
def google_page():
	return render_template("google.html")

@application.route("/vote/<electionid>", methods=['GET', 'POST'])
def cast_vote(electionid):
	# if not cas.username:
	# 	return redirect(url_for(route_home))
	if request.method=='POST':
		cur = g.db.execute('select id from elections where id=(?)',[electionid])
		if len(cur.fetchall()) == 0:
			return redirect(url_for('vote_page', error="Sorry that election does not exist. Here are some that might though."))
		something = dict(request.form)
		cur = g.db.execute('select username from voted where electionid = (?) and username= (?)', [electionid, cas.username])
		if len(cur.fetchall()) > 0:
			return redirect(url_for('vote_page', error="Sorry you cannot vote again"))
		for key,value in something.iteritems():
			cur2 = g.db.execute('select votes from candidates where id=(?)', [key] )
			fetched = [dict(votes=row[0]) for row in cur2.fetchall()]
			num_votes = fetched[0]['votes']+1
			g.db.execute('update candidates set votes=(?) where id=(?)', [num_votes, key])
			g.db.commit()

		g.db.execute('insert into voted (electionid, username) values ((?), (?))', [electionid, cas.username])
		g.db.commit()
		return redirect(url_for('vote_page', thankyou="Thank you for voting!"))


application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	application.run(debug=True, host='0.0.0.0')







	
