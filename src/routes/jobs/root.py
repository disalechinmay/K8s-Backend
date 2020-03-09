from __main__ import app, batchv1
from flask import jsonify, request
import json
from pprint import pprint 

# Usage: Returns a list of all jobs present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/jobs', methods = ['GET'])
def getjobs():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    alljobs = batchv1.list_namespaced_job(namespace).to_dict()
    pprint(alljobs)
    returnList = []

    for job in alljobs["items"]:
        tempDict = {}
        tempDict["jobName"] = job["metadata"]["name"]
        tempDict["jobLabels"] = job["metadata"]["labels"]
        tempDict["jobAnnotations"] = job["metadata"]["annotations"]
        tempDict["jobContainers"] = []
        tempDict["jobCurrentCompletions"] = job["status"]["succeeded"]

        for container in job["spec"]["template"]["spec"]["containers"]:
            tempDict["jobContainers"].append(container["image"])      
        print("dsfsfd")
        tempDict["jobTargetCompletions"] = job["spec"]["completions"]
        tempDict["jobStartTime"] = job["status"]["start_time"] 
        tempDict["jobCompletionTime"] = job["status"]["completion_time"] 
        returnList.append(tempDict)

    print("fasfas")
    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning a list of jobs of '" + namespace + "' namespace.",
        payLoad = returnList
    )

