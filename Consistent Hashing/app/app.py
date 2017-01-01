from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from model import db
from model import User
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
# from sqlalchemy.orm import sessionmaker


# initate flask app
app = Flask(__name__)

# http://localhost
@app.route('/')
def index():
	return 'This is cmpe273-Assignment1 - Application1\n'

@app.route('/v1')
def welcome():
	return 'Welcome to Assignment 1.\n\nThis basic app is developer as a part of CMPE 273 Assignment. You should be able to run below tests on this application\n# POST should be working on /v1/expenses\n# checking GET on /v1/expenses/{id}\n# checking GET for invalid id\n# checking for put on /v1/expenses/{id}\n# checking if values have changed after PUT\n# checking for delete at /v1/expenses/{id}\n# checking if object still exists \n\n\n Please continue testing this as you wish!!!'


# POST method to create a user in database
@app.route('/v1/expenses/', methods=['POST'])
def insert_user():
	# if request.method == 'POST':
	try:
		x = request.get_json(force=True)
		user = User(x['id'],
				x['name'],
				x['email'],
				x['category'],
				x['description'],
				x['link'],
				x['estimated_costs'],
				x['submit_date'])
		db.session.add(user)
		db.session.commit()
		resp = jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category,'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': str(user.submit_date), 'status': user.status, 'decision_date': str(user.decision_date)})
		resp.status_code=201
		db.session.remove()
		return resp
	except IntegrityError:
		db.session.rollback()
		return jsonify({})

	# elif request.method == 'GET':
	# 	try:
	# 		user1 = User.query.all()
	# 		user = user1[8]
	# 		get = jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category,'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': str(user.submit_date), 'status': user.status, 'decision_date': str(user.decision_date)})
	# 		get.status_code=200
	# 		return get
	# 	except IntegrityError:
	# 		return jsonify({})
		# try:
		# 	user = User.query.all()
		# 	print user
		# 	get = jsonify(dict(r) for r in {'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category,'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': str(user.submit_date), 'status': user.status, 'decision_date': str(user.decision_date)})
		# 	get.status_code=200
		# 	return get
		# except IntegrityError:
		# 	return jsonify({})
# GET method to retrieve user from database
@app.route('/v1/expenses/<id>', methods=['GET'])
def show_user(id):
	try:
		user = User.query.filter_by(id=id).first_or_404()
		get = jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category,'description': user.description, 'link': user.link, 'estimated_costs': user.estimated_costs, 'submit_date': str(user.submit_date), 'status': user.status, 'decision_date': str(user.decision_date)})
		get.status_code=200
		return get
	except IntegrityError:
		return jsonify({})


#PUT method to update estimated cost in database
@app.route('/v1/expenses/<id>', methods=['PUT'])
def update_expense(id):
	try:
		user = User.query.filter_by(id=id).first_or_404()
		db.session.add(user)
		db.session.commit()
		x = request.get_json(force=True)
		user.estimated_costs = x['estimated_costs']
		put = jsonify({"message": "success"})
		put.status_code=202
		# db.session.remove()
		return put
	except IntegrityError:
		return jsonify({})

#  DELETE method to remove an entry from database
@app.route('/v1/expenses/<id>', methods=['DELETE'])
def delete_row(id):
	try:
		user = User.query.filter_by(id=id).first_or_404()
		db.session.delete(user)
		db.session.add()
		db.session.commit()
		dele = jsonify({})
		dele.status_code=204
		db.session.remove()
		return dele
	except IntegrityError:
		return jsonify({})

# run app service
if __name__ == "__main__":
	CreateDB()  # create database
	db.create_all()  # create db tables
	app.run(host="0.0.0.0", port=5000, debug=True)
