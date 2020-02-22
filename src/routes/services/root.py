from __main__ import app, v1, cross_origin
from flask import jsonify, request
import json

# Usage: Returns a list of all services present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/servicesx', methods = ['GET'])
@cross_origin(supports_credentials = True)
def getServices():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allServices = v1.list_namespaced_service(namespace).to_dict()

	returnList = []

	for service in allServices["items"]:
		tempDict = {}
		tempDict["serviceName"] = service["metadata"]["name"]
		tempDict["serviceType"] = service["spec"]["type"]
		tempDict["serviceLabels"] = service["metadata"]["labels"]
		tempDict["serviceAnnotations"] = service["metadata"]["annotations"]
		tempDict["serviceSelectors"] = service["spec"]["selector"]
		tempDict["servicePort"] = []
		tempDict["serviceTargetPort"] = []

		for port in service["spec"]["ports"]:
			tempDict["servicePort"].append(port["port"])
			tempDict["serviceTargetPort"].append(port["target_port"])

		returnList.append(tempDict)

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /servicesx endpoint.",
		payLoad = returnList
	)
