# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return db.reversibleEncrypt('decrypt',session['email']) if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html',user=getUser())

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/home')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	status = db.authenticate(email=form_fields['email'],password=form_fields['password'])
	
	if (status['success'] == 1):
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
		return json.dumps({'success':1})
	else:
		return json.dumps({'success':0})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')


		
# @socketio.on('messaged', namespace='/chat')
# def messaged(message):
# 	pass
#######################################################################################
# OTHER
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x  = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html',user=getUser(), class_name = "Main-Text")


@app.route('/projects')
def projects():
	return render_template('projects.html',user=getUser(),class_name = "Main-Text")


@app.route('/piano')
def piano():
	return render_template('piano.html',user=getUser(),class_name = "Piano-Project")

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html',user=getUser(), resume_data = resume_data)


@app.route('/processfeedback',methods=['POST'])
def feedback():
	print(request.form.to_dict())
	name = request.form.get("name")
	email = request.form.get("email")
	comment = request.form.get("feedback")
	db.query(query="INSERT INTO `feedback` (`name`,`email`,`comment`) VALUES (%s,%s,%s)",parameters=[name,email,comment])
	feedback_data = db.query(query="SELECT * FROM feedback")
	input_data = {}
	for row in feedback_data:
		comment_id = row["comment_id"]
		row_name = row["name"]
		row_email = row["email"]
		row_comment = row["comment"]
		input_data[comment_id] = {"name":row_name,"email":row_email,"comment":row_comment}
	return render_template('processfeedback.html',user=getUser(),user_feedback=input_data)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
