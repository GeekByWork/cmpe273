from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from datetime import *



# Database Configurations
app = Flask(__name__)
DATABASE = 'test'
PASSWORD = 'mysql'
USER = 'root'
HOSTNAME = 'mysqlserver'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)


class User(db.Model):

	# Data Model User Table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=False)
	email = db.Column(db.String(120), unique=False)
	category = db.Column(db.String(120), unique=False)
	description = db.Column(db.String(240), unique=False)
	link = db.Column(db.String(480), unique=False)
	estimated_costs = db.Column(db.String(80), unique=False)
	submit_date = db.Column(db.String(80), unique=False)
	status = db.Column(db.String(120), unique=False)
	decision_date = db.Column(db.String(80), unique=False)

	def __init__(self, id, name, email, category, description, link, estimated_costs, submit_date):
		# initialize columns
		self.id = id
		self.name = name
		self.email = email
		self.category = category
		self.description = description
		self.link = link
		self.estimated_costs = estimated_costs
		self.submit_date = submit_date
		self.status = "pending"
		self.decision_date = str(datetime.utcnow().strftime('%m-%d-%Y'))

	def __repr__(self):
		return '<User %r>' % self.name

class CreateDB():
	def __init__(self):
		import sqlalchemy
		engine = sqlalchemy.create_engine('mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)) # connect to server
		engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

if __name__ == '__main__':
	Manager.run()
