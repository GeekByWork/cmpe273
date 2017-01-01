from flask import Flask, request, abort,jsonify
from ConsistentHashRing import ConsistentHashRing
import simplejson as json
import requests

app = Flask(__name__)
consistentHashRing = ConsistentHashRing(False)
consistentHashRing.addnode("1", "127.0.0.1:5001")
consistentHashRing.addnode("2", "127.0.0.1:5002")
consistentHashRing.addnode("3", "127.0.0.1:5003")

@app.route('/')
def index():
    return "This is a consistent hashing ring client"

@app.route('/v1/expenses', methods=['POST'])
def redirect_post():
    content = json.loads(request.data)
    if not content or not 'name' in content:
        abort(404)
    node = consistentHashRing.getnode(str(content['id']))
    print node
    r = requests.post("http://"+node+"/v1/expenses/", data=json.dumps(content))
    print r.text
    return r.text +"\n"+ r.url


@app.route('/v1/expenses/<expense_id>', methods=['GET'])
def redirect_get(expense_id):
    node = consistentHashRing.getnode(str(expense_id))
    r = requests.get("http://"+node+"/v1/expenses/"+expense_id)
    print r.text
    return  "Server " + r.url.split("/")[2] + " returns:\n\n" + r.text + "\n*************************\n"

# run app service
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5010, debug=True)
