# Read APIRef.txt before working on this repo.

from flask import Flask, jsonify
from kubernetes import client, config
from flask_cors import CORS

# Use config.load_incluster_config() for incluster deployment.
# Else use config.load_kube_config()  <-- USE FOR DEV
config.load_kube_config()

v1 = client.CoreV1Api()
appsv1 = client.AppsV1Api()

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


from src.routes.services import *
from src.routes.deployments import *
from src.routes.pods import *
from src.routes.nodes import *
from src.routes.namespaces import *

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
		), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
