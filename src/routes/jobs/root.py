from __main__ import app, appsv1, batchv1, cross_origin
from flask import jsonify, request
import json


@app.route('/jobs', methods=['GET'])
@cross_origin(supports_credentials=True)
def getjobs():
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"
    alljobs = batchv1.list_namespaced_job(namespace).to_dict()
    print(alljobs)
    returnList = []

    for jobs in alljobs["items"]:
        tempDict = {}
        tempDict["jobName"] = jobs["metadata"]["name"]
        tempDict["jobLabels"] = jobs["metadata"]["labels"]
        tempDict["jobAnnotations"] = jobs["metadata"]["annotations"]
        tempDict["jobStatus"] = []
        tempDict["jobTemplate"] = []

        print()
        print("\nSPEC->template->spec")
        for container in jobs["spec"]["template"]["spec"]["containers"]:
            tempDict["jobTemplate"].append(container["image"])

        for status in jobs["status"]["conditions"]:
            tempDict["jobStatus"].append(status["type"])
        returnList.append(tempDict)

    return jsonify(
        status="SUCCESS",
        statusDetails="Returning data from /jobs endpoint.",
        payLoad=returnList,

    )
