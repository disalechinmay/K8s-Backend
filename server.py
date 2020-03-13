# Read APIRef.txt before working on this repo.
from flask import Flask, jsonify, make_response
from kubernetes import client, config
import json

app = Flask(__name__)

# Middleware to hanndle cross origin requests
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS,PUT')
  return response

# Use config.load_incluster_config() for incluster deployment.
# Else use config.load_kube_config()  <-- USE FOR DEV
config.load_kube_config()

v1 = client.CoreV1Api()
appsv1 = client.AppsV1Api()
batchv1 = client.BatchV1Api()
batchv1beta1 = client.BatchV1beta1Api()

# Importing all endpoints from /src/routes
from src.routes.secrets import *
from src.routes.configmaps import *
from src.routes.secrets import *
from src.routes.cronjobs import *
from src.routes.jobs import *
from src.routes.services import *
from src.routes.deployments import *
from src.routes.pods import *
from src.routes.nodes import *
from src.routes.namespaces import *


# Handles invalid API endpoints
@app.errorhandler(404)
def pageNotFound(error):
	return jsonify(
			status = "FAILURE", 
			statusDetails = "You have reached an invalid endpoint.",
			payLoad = {
				"errorCode": error.code,
				"errorName": error.name,
				"errorDescription": error.description
			}
		), 404

# Handles internal server errors
@app.errorhandler(Exception)
def internalServerError(error):
	print(error)
	return jsonify(
			status = "FAILURE", 
			statusDetails = "An internal server error has occurred.",
			payLoad = {
				"errorCode": 500,
				"errorName": "Internal Server Error",
				"errorDescription": str(error)
			}
		), 500

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
