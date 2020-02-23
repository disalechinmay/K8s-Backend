from __main__ import app, batchv1, cross_origin
from flask import jsonify, request
import json

# Usage: Returns a list of all jobs present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/jobs', methods = ['GET'])
@cross_origin(supports_credentials = True)
def getjobs():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    alljobs = batchv1.list_namespaced_job(namespace).to_dict()
    
    returnList = []

    for jobs in alljobs["items"]:
        tempDict = {}
        tempDict["jobName"] = jobs["metadata"]["name"]
        tempDict["jobLabels"] = jobs["metadata"]["labels"]
        tempDict["jobAnnotations"] = jobs["metadata"]["annotations"]
        tempDict["jobStatus"] = []
        tempDict["jobTemplate"] = []

        for container in jobs["spec"]["template"]["spec"]["containers"]:
            tempDict["jobTemplate"].append(container["image"])

        for status in jobs["status"]["conditions"]:
            tempDict["jobStatus"].append(status["type"])

        returnList.append(tempDict)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning data from /jobs endpoint.",
        payLoad = returnList
    )
