from flask import Flask
from flask import request
import requests
import redis
import json
import ipdb

application = Flask(__name__)
rds = redis.Redis()


@application.route("/api/request/", methods=["GET"])
def api_request():
	data = request.values.to_dict()
	# checking for connid
	try:
		connId = data['connId']
	except:
		return json.dumps({"status": "Fail", "error": "connId missing"})

	# checking for timeout
	try:
		timeout = data['timeout']
	except:
		return json.dumps({"status": "Fail", "error": "timeout missing"})

	rds.setex(connId, True, timeout)
	while(rds.get(connId) == 'True'):
		pass

	try:
		resp = rds.get(connId)
		if resp == 'False':
			rds.delete(connId)	
			return json.dumps({"status": "killed"})
		else:
			return json.dumps({"status": "ok"})
	except:
		return json.dumps({"status": "ok"})
	


@application.route("/api/serverStatus/", methods=["GET"])
def api_serverStatus():
	keys = rds.keys()
	resp = {}
	for key in keys:
		resp[key] = rds.ttl(key)
	return json.dumps(resp)



@application.route("/api/kill/", methods=["PUT"])
def api_kill():
	data = request.form
	try:
		connId = data['connId']
	except:
		return json.dumps({"status": "Fail", "error": "connId missing"})

	
	resp = rds.get(connId)
	if resp:
		rds.set(connId, False)	
		return json.dumps({"status": "ok"})
	else:
		return json.dumps({"status": "invalid connection id: " + connId})



if __name__ == "__main__":
	try:
		if rds.ping() == False:
			print "Couldn't connect to redis server"
		application.run(debug=True)
	except:
		print "Couldn't connect to redis server"

