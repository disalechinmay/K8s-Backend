from __main__ import app
from __main__ import v1
from flask import jsonify, request
import json

@app.route('/services/', methods=['GET'])
def getServices():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allServices = v1.list_namespaced_service(namespace).to_dict()

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /services/ endpoint.",
		payLoad = allServices
		)
