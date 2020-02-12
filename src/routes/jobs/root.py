from __main__ import app
from __main__ import appsv1
from __main__ import batchv1
from flask import jsonify, request
import json

@app.route('/jobs/', methods=['GET'])
def getjobs():
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"
    alljobs =batchv1.list_namespaced_job(namespace).to_dict()
    print(alljobs)
    returnList=[]
    
    for jobs in alljobs["items"]:
        tempDict = {}
        tempDict["jobName"]=jobs["metadata"]["name"]
        returnList.append(tempDict)


    return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /jobs/ endpoint.",
		payLoad = returnList,
		
		)

