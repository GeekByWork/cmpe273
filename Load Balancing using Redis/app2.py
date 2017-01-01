import redis
from flask import json, Response
from flask import Flask
from flask_sqlalchemy import *

app =Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:root@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
db = SQLAlchemy(app)
DATABASE='test'

class DBTEST(db.Model):
    __tablename__ = 'sampleTable'
    id = db.Column('id', db.Integer, primary_key = 'True')
    name = db.Column('name',db.String(20))
    email = db.Column('email', db.String(20))
    category = db.Column('category', db.String(20))
    description = db.Column('description', db.String(2000))
    link = db.Column('link', db.String(300))
    estimated_costs = db.Column('estimated_costs', db.String(20))
    submit_date = db.Column('submit_date', db.String(20))
    status = db.Column('status', db.String(20))
    decision_date = db.Column('decision_date', db.String(200))

    def __init__(self,name= '', email='',category='',description='',link='',estimated_costs='',submit_date='',status='',decision_date=''):
        self.name= name
        self.email = email
        self.category= category
        self.description= description
        self.link= link
        self.estimated_costs= estimated_costs
        self.submit_date= submit_date
        self.status= status
        self.decision_date=decision_date

class Createdatabase():
    engine = sqlalchemy.create_engine('mysql://root:root@localhost/test')
    engine.execute("CREATE DATABASE IF NOT EXISTS %s; " %(DATABASE))
    engine.execute("USE test ;")
    db.create_all()
    db.session.commit()

@app.route('/v1/expenses/<int:req_id>', methods=['GET'])
def index(req_id):
    one = DBTEST.query.filter_by(id=req_id).first()
    if one is not None:
        a = {
            "id": one.id,
            "name": one.name,
            "email": one.email,
            "category": one.category,
            "description": one.description,
            "link": one.link,
            "submit_date": one.submit_date,
            "estimated_costs": one.estimated_costs,
            "status": one.status,
            "decision_date": one.decision_date}
        b = Response(response=json.dumps(a), status=200)
        return b
    else:
        b = Response(status=404)
        return b


@app.route('/v1/expenses', methods=['POST'])
def postrequest():
    a = request.get_json(force=True)

    name = a['name']
    email = a['email']
    category = a['category']
    description = a['description']
    link = a['link']
    estimated_costs = a['estimated_costs']
    submit_date = a['submit_date']
    status = "pending"
    decision_date = ""

    row = DBTEST(name, email, category, description, link, estimated_costs, submit_date, status, decision_date)
    db.session.add(row)
    db.session.commit()

    a = {'id': row.id,
           'name': row.name,
           'email': row.email,
           'category': row.category,
           'description': row.description,
           'link': row.link,
           'estimated_costs': row.estimated_costs,
           'submit_date': row.submit_date,
           'status': row.status,
           'decision_date': row.decision_date
           }
    b = Response(response=json.dumps(a), status=201, mimetype="application/json")
    return b

@app.route('/v1/expenses/<int:requestID>', methods=['PUT'])
def putmethod(requestID):
    a = request.get_json(force=True)
    updateRow = DBTEST.query.filter_by(id=requestID)
    if (updateRow != None):
        for key, value in a.items():
            updateRow.update({key: value})
            db.session.commit()
            b = Response(status=202)
            return b

@app.route('/v1/expenses/<int:req_id>', methods=['DELETE'])
def deleterequest(req_id):
    a= db.session.query(DBTEST).filter_by(id=req_id).first()
    if a is not None:
        db.session.delete(a)
        db.session.commit()
        return (Response(status=204))

if __name__ == "__main__":
    r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
    r.set(2, '5002')
    app.run(debug=True, host='0.0.0.0', port=5002)