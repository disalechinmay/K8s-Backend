from __main__ import app, batchv1beta1
from flask import jsonify, request
import json
from pprint import pprint 

# Usage: Returns a list of all cron jobs present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/cronjobs', methods = ['GET'])
def getCronJobs():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    allJobs = batchv1beta1.list_namespaced_cron_job(namespace).to_dict()
    returnList = []
    pprint(allJobs)
    for job in allJobs["items"]:
        tempDict = {}
        tempDict["jobName"] = job["metadata"]["name"]
        tempDict["jobLabels"] = job["metadata"]["labels"]
        tempDict["jobAnnotations"] = job["metadata"]["annotations"]
        tempDict["jobSchedule"] = job["spec"]["schedule"]
        tempDict["jobContainers"] = []

        for container in job["spec"]["job_template"]["spec"]["template"]["spec"]["containers"]:
            tempDict["jobContainers"].append(container["image"])      
        
        tempDict["jobLastScheduled"] = job["status"]["last_schedule_time"]
        returnList.append(tempDict)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning a list of jobs of '" + namespace + "' namespace.",
        payLoad = returnList
    )


@app.route('/cronjob', methods = ['GET'])
def getCronJob():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    cronJobName = request.args.get("cronJobName")

    if (namespace is None) and (cronJobName is None):
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

    if(cronJobName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Cron Job name is not specified as query params.",
            payLoad = None
        )


    cronJob = batchv1beta1.read_namespaced_cron_job(namespace = namespace, name = cronJobName).to_dict()

  
    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning cron job '" + cronJobName + "' of '" + namespace + "' namespace.",
        payLoad = cronJob
    )





@app.route('/cronjob', methods = ['DELETE'])
def deleteCronJob():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    if (requestJSON["namespace"] is None) and (requestJSON["cronJobName"] is None):
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

    if(requestJSON["cronJobName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Cron Job name is not specified as body params.",
            payLoad = None
        )


    returnValue = batchv1beta1.delete_namespaced_cron_job(
            requestJSON["cronJobName"], requestJSON["namespace"]
        ).to_dict()


    return jsonify(
        status = "SUCCESS",
        statusDetails = "Attempted to delete job '" + requestJSON["cronJobName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
        payLoad = None
    )


@app.route('/cronjob', methods = ['PATCH'])
def patchCronJob():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = batchv1beta1.patch_namespaced_cron_job(
                namespace = requestJSON["namespace"],
                name = requestJSON["cronJobName"], body = requestJSON["body"]
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

