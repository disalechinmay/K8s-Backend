# Read APIRef.txt before working on this repo.
from flask import Flask, jsonify, make_response
from kubernetes import client, config
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Use config.load_incluster_config() for incluster deployment.
# Else use config.load_kube_config()  <-- USE FOR DEV
config.load_kube_config()

v1 = client.CoreV1Api()
appsv1 = client.AppsV1Api()
batchv1 = client.BatchV1Api()

# Importing all endpoints from /src/routes
from src.routes.jobs import *
from src.routes.services import *
from src.routes.deployments import *
from src.routes.pods import *
from src.routes.nodes import *
from src.routes.namespaces import *

# Endpoint to handle invalid API endpoints
@app.errorhandler(404)
def pageNotFound(e):
	return jsonify(
			status = "FAILURE", 
			statusDetails = "You have reached an invalid endpoint.",
			payLoad = None
		), 404

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
