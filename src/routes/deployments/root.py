from __main__ import app
from __main__ import appsv1
from flask import jsonify, request
import json

@app.route('/deployments/', methods=['GET'])
def getDeployments():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allDeployments = appsv1.list_namespaced_deployment(namespace).to_dict()

	returnList = []

	for deployment in allDeployments["items"]:
		tempDict = {}
		tempDict["deploymentName"] = deployment["metadata"]["name"]
		tempDict["deploymentLabels"] = deployment["metadata"]["labels"]
		tempDict["deploymentAnnotations"] = deployment["metadata"]["annotations"]
		tempDict["deploymentReplicas"] = deployment["spec"]["replicas"]
		tempDict["deploymentSelectors"] = {}

		# Clubbing all kinds of selectors into deploymentSelectors
		if deployment["spec"]["selector"]["match_expressions"]:
			for key, value in deployment["spec"]["selector"]["match_expressions"].items():
				tempDict["deploymentSelectors"][key] = value
		if deployment["spec"]["selector"]["match_labels"]:
			for key, value in deployment["spec"]["selector"]["match_labels"].items():
				tempDict["deploymentSelectors"][key] = value

		tempDict["deploymentTemplateLabels"] = {}
		if deployment["spec"]["template"]["metadata"]["labels"]:
			for key, value in deployment["spec"]["template"]["metadata"]["labels"].items():
				tempDict["deploymentTemplateLabels"][key] = value

		tempDict["deploymentTemplateContainers"] = []		
		for container in deployment["spec"]["template"]["spec"]["containers"]:
			tempDict["deploymentTemplateContainers"].append(container["image"])



		returnList.append(tempDict)


	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /deployments/ endpoint.",
		payLoad = returnList,
		raw = allDeployments
		)
