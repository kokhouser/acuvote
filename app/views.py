from flask import render_template, flash, redirect, session, url_for,request
from app import app
from flask.ext.cas import CAS
from flask.ext.cas import login_required

@app.route("/")
@login_required
def route_home():
	return (cas.username)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

	