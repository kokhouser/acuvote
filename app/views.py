from flask import render_template, flash, redirect, session, url_for,request
from app import application
from flask.ext.cas import CAS
from flask.ext.cas import login_required

@application.route("/")
@login_required
def route_home():
	return (cas.username)

application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

	