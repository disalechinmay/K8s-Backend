from __main__ import app
from __main__ import v1
from flask import jsonify
import json

@app.route('/nodes/', methods=['GET'])
def getNodes():

	allNodes = v1.list_node().to_dict()

	returnList = []

	for node in allNodes["items"]:
		tempDict = {}
		tempDict["nodeName"] = node["metadata"]["name"]
		tempDict["nodeLabels"] = node["metadata"]["labels"]
		tempDict["nodeAnnotations"] = node["metadata"]["annotations"]
		tempDict["nodeCapacity"] = node["status"]["capacity"]

		returnList.append(tempDict)

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /nodes/ endpoint.",
		payLoad = returnList
		)
