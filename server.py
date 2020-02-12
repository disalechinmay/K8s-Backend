# Read APIRef.txt before working on this repo.

from flask import Flask, jsonify, make_response
from kubernetes import client, config
from flask_cors import CORS

# Use config.load_incluster_config() for incluster deployment.
# Else use config.load_kube_config()  <-- USE FOR DEV
config.load_kube_config()

v1 = client.CoreV1Api()
appsv1 = client.AppsV1Api()
# batchv1=client.BatchV1Api()
batchv1 = client.BatchV1Api()

from flask_cors import CORS

app = Flask(__name__)

@

# @app.after_request
# def after_request(response):
# 	print("INSIDE")
# 	print(response.headers)
# 	response.headers.add('Access-Control-Allow-Origin', '*')
# 	response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
# 	response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
# 	print(response.headers)
# 	return response

from src.routes.services import *
from src.routes.deployments import *
from src.routes.pods import *
from src.routes.nodes import *
from src.routes.namespaces import *
from src.routes.jobs import *

@app.route('/test')
def testRoute():
    return jsonify(
    	status = "SUCCESS",
    	statusDetails = "Returning data from /test endpoint.",
    	payLoad = "Testing /test endpoint."
    	)

@app.errorhandler(404)
def pageNotFound(e):
	return jsonify(
		status = "FAILURE", 
		statusDetails = "You have reached an invalid endpoint.",
		payLoad = None
		)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
