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
	return render_template('login.html',user=getUser(),class_name = "Main-Text")

@app.route('/board_creation')
@login_required
def board_creation():
      return render_template('board_creation.html',user=getUser(),class_name = "Main-Text")

@app.route('/signup')
def signup():
      return render_template('signup.html',user=getUser(),class_name = "Main-Text")

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/login')

@app.route('/processlogin', methods = ["POST","GET"])
def processlogin():
	form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
	status = db.authenticate(email=form_fields['email'],password=form_fields['password'])
	
	if (status['success'] == 1):
		session['email'] = db.reversibleEncrypt('encrypt', form_fields['email']) 
		return json.dumps({'success':1})
	else:
		return json.dumps({'success':0})
      
@app.route('/processsignup', methods = ["POST","GET"])
def processsignup():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    email = form_fields['email']
    password = form_fields['password']

    db.createUser(email=email,password=password)
    return json.dumps({'success':1})

@app.route('/processBoardCreation', methods = ["POST"])
def processBoardCreation():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    
    name = form_fields["boardName"]

    #["email1","email2"]....
    emails = (form_fields["allowedEmails"]).split(",")
    return_val = db.CreateBoard(name=name,emails=emails)
    
    # print("Test for board creation")
    # print(db.query("SELECT * FROM boardgroups;"))
    # print(db.query("SELECT * FROM boards;"))
    return json.dumps(return_val)


#######################################################################################
# CHATROOM RELATED
#######################################################################################

@app.route('/home')
@login_required
def home():
    return render_template('home.html',user=getUser(), class_name = "Main-Text")

@app.route('/board_display/<int:board_id>')
def board_display(board_id):
    board_data = db.GetBoardData(board_id=board_id)
    print(board_data)
    return render_template('board_display.html',user=getUser(), board_data=board_data, class_name = "Main-Text",board_id=board_id)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
@login_required
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
	return redirect("/home")

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


#######################################################################################
# CARD RELATED
#######################################################################################
@app.route('/processCardCreation', methods = ["POST"])
def processCardCreation():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    
    name = form_fields["CardName"]
    body = form_fields["CardBody"]
    type = form_fields["CardType"]
    id   = form_fields["BoardId"]
    
    db.insertRows(table="cards",columns=['board_id','card_text','card_title','card_list'],parameters=[[id,body,name,type]])
    card_id = (db.query(query="SELECT MAX(card_id) FROM cards WHERE board_id = %s;",parameters=[id]))[0]["MAX(card_id)"]
    print(card_id)
    socketio.emit('card_added', {
        'card_id': card_id,
        'card_title': name,
        'card_text': body,
        'card_list': type,
        'board_id': id
    })

    return json.dumps({'success':1})


@app.route('/processCardDeletion', methods = ["POST"])
def processCardDeletion():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    card_id   = form_fields["CardId"]
    print("Delete Called")
    print(card_id)
    db.query(query="DELETE FROM cards WHERE card_id = %s",parameters=[card_id])
    print(db.query(query="SELECT * FROM cards"))

    socketio.emit('card_deleted', {
        'card_id': card_id,
    })
    return json.dumps({'success':1})

@app.route('/processCardEdit', methods = ["POST"])
def processCardEdit():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    card_id   = form_fields["CardId"]
    card_text = form_fields["CardText"]
    db.query(query="UPDATE cards SET card_text = %s WHERE card_id = %s",parameters=[card_text,card_id])
    socketio.emit('card_edited', {
        'card_id': card_id,
        'body_content': card_text
    })
    return json.dumps({'success':1})


@app.route('/processCardMovement', methods = ["POST"])
def processCardMovement():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    card_id   = form_fields["CardId"]
    new_column = form_fields["NewColumn"]
    old_column = db.query(query="SELECT card_list FROM cards WHERE card_id = %s",parameters=[card_id])
    db.query(query="UPDATE cards SET card_list = %s WHERE card_id = %s",parameters=[new_column,card_id])
    socketio.emit('card_moved', {
         'card_id': card_id,
         'new_column': new_column,
         'old_column':old_column
    })
    return json.dumps({'success':1})


