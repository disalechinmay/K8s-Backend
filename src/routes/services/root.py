from __main__ import app
from __main__ import v1
from flask import jsonify, request
import json

@app.route('/servicesx', methods=['GET'])
def getServices():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allServices = v1.list_namespaced_service(namespace).to_dict()

	returnList = []

	for service in allServices["items"]:
		tempDict={}
		tempDict["serviceName"]=service["metadata"]["name"]
		tempDict["serviceType"]=service["spec"]["type"]
		tempDict["serviceLabels"] = service["metadata"]["labels"]
		tempDict["serviceAnnotations"] = service["metadata"]["annotations"]
		# if service["spec"]["selector"]["match_expressions"]:
		# 	for key, value in service["spec"]["selector"]["match_expressions"].items():
		# 		tempDict["serviceSelectors"][key] = value
		tempDict["serviceSelectors"]=service["spec"]["selector"]
		tempDict["servicePort"]=[]
		tempDict["serviceTargetPort"]=[]
		for port in service["spec"]["ports"]:
			tempDict["servicePort"].append(port["port"])
			print(port)
			tempDict["serviceTargetPort"].append(port["target_port"])
		
		# for port in service["spec"]["ports"]:
			# tempDict["serviceTargetPort"].append(port["targetPort"])


		returnList.append(tempDict)


	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /services endpoint.",
		payLoad = returnList
		)
