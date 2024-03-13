# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x  = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
	return render_template('home.html', class_name = "Main-Text")


@app.route('/projects')
def projects():
	return render_template('projects.html',class_name = "Main-Text")


@app.route('/piano')
def piano():
	return render_template('piano.html',class_name = "Piano-Project")

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)


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
	return render_template('processfeedback.html',user_feedback=input_data)