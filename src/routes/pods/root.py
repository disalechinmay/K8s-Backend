from __main__ import app
from __main__ import v1
from flask import jsonify, request
import json

@app.route('/pods/', methods=['GET'])
def getPods():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allPods = v1.list_namespaced_pod(namespace).to_dict()

	returnList = []

	for pod in allPods["items"]:
		tempDict = {}
		tempDict["podName"] = pod["metadata"]["name"]
		tempDict["podLabels"] = pod["metadata"]["labels"]
		tempDict["podAnnotations"] = pod["metadata"]["annotations"]
		tempDict["podContainers"] = []

		for container in pod["spec"]["containers"]:
			tempDict["podContainers"].append(container["image"])

		returnList.append(tempDict)


	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /pods/ endpoint.",
		payLoad = returnList
		)
