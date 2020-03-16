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
        
        tempDict["jobTargetCompletions"] = job["spec"]["completions"]
        tempDict["jobStartTime"] = job["status"]["start_time"] 
        tempDict["jobCompletionTime"] = job["status"]["completion_time"] 
        returnList.append(tempDict)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning a list of jobs of '" + namespace + "' namespace.",
        payLoad = returnList
    )

@app.route('/job', methods = ['DELETE'])
def deleteJob():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    if (requestJSON["namespace"] is None) and (requestJSON["jobName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & Job name is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["namespace"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["jobName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Job name is not specified as body params.",
            payLoad = None
        )


    returnValue = batchv1.delete_namespaced_job(
            requestJSON["jobName"], requestJSON["namespace"]
        ).to_dict()


    return jsonify(
        status = "SUCCESS",
        statusDetails = "Attempted to delete job '" + requestJSON["jobName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
        payLoad = None
    )


@app.route('/job', methods = ['PATCH'])
def patchJob():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = batchv1.patch_namespaced_job(
                namespace = requestJSON["namespace"],
                name = requestJSON["jobName"], body = requestJSON["body"]
            )

        return jsonify(
            status = "SUCCESS",
            statusDetails = "Cron Job patched successfully.",
            payLoad = result.to_dict()
        )
        
    except Exception as e:
        return jsonify(
                status = "FAILURE",
                statusDetails = "Pod patch failed.",
                payLoad = json.loads(e.body) if e.body else str(e)
            )


@app.route('/job', methods = ['GET'])
def getJob():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    jobName = request.args.get("jobName")

    if (namespace is None) and (jobName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & pod name is not specified as query params.",
            payLoad = None
        )

    if(namespace is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as query params.",
            payLoad = None
        )

    if(jobName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Cron Job name is not specified as query params.",
            payLoad = None
        )


    job = batchv1.read_namespaced_job(namespace = namespace, name = jobName).to_dict()

  
    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning cron job '" + jobName + "' of '" + namespace + "' namespace.",
        payLoad = job
    )

