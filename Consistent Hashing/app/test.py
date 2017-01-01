from ConsistentHashRing import ConsistentHashRing
import requests

consistentHashRing = ConsistentHashRing(False)
consistentHashRing.addnode("1", "127.0.0.1:5001")
consistentHashRing.addnode("2", "127.0.0.1:5002")
consistentHashRing.addnode("3", "127.0.0.1:5003")

dict = {}

for i in xrange(1,11):
    node = consistentHashRing.getnode(str(i))
    r = requests.get("http://127.0.0.1:5010/v1/expenses/"+str(i))
    print "http://127.0.0.1:5010/v1/expenses/"+str(i)
    print r.status_code

    server = consistentHashRing.getnode(str(i))
    if server not in dict:
        dict[server] = 1
    dict[server] += 1

print 'The summary is:\n'
print dict
