from __main__ import app, v1, cross_origin
from flask import jsonify
import json

# Usage: Returns a list of all nodes present in the cluster.
# Method: GET
# Params: None
@app.route('/nodes', methods = ['GET'])
@cross_origin(supports_credentials = True)
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
        statusDetails = "Returning data from /nodes endpoint.",
        payLoad = returnList
    )
