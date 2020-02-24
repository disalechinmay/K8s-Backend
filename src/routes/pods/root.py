from __main__ import app, v1
from flask import jsonify, request
import json

# Usage: Returns a list of all pods present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/pods', methods = ['GET'])
def getPods():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    allPods = v1.list_namespaced_pod(namespace).to_dict()

    returnList = []

    for pod in allPods["items"]:
        tempDict = {}
        tempDict["podName"] = pod["metadata"]["name"]
        tempDict["podLabels"] = pod["metadata"]["labels"]
        tempDict["podAnnotations"] = pod["metadata"]["annotations"]
        tempDict["podStatus"] = pod["status"]["phase"]
        tempDict["podContainers"] = []

        for container in pod["spec"]["containers"]:
            tempDict["podContainers"].append(container["image"])

        returnList.append(tempDict)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning data from /pods endpoint.",
        payLoad = returnList
    )

# Usage: Deletes a pod by podName & namespace specified in request.
# Method: DELETE
# Request Body: JSON {
#                        podName: "",
#                        namespace: ""
#                    }
@app.route('/pods', methods = ['POST'])
def deletePod():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    retVal = v1.delete_namespaced_pod(
            requestJSON["podName"], requestJSON["namespace"]
        ).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning from /pods endpoint.",
        payLoad = retVal
    )

# Usage: Returns list of exposures by podName & namespace specified in request.
# Method: GET
# Params: namespace, podName
@app.route('/pods/exposure', methods = ['GET'])
def getPodExposure():

    namespace = request.args.get("namespace")
    podName = request.args.get("podName")

    allServices = v1.list_namespaced_service(namespace).to_dict()
    
    podInfo = v1.read_namespaced_pod(name = podName, namespace = namespace).to_dict()
    podLabels = podInfo["metadata"]["labels"]

    exposures = []

    for service in allServices["items"]:
        selectors = service["spec"]["selector"]
        if selectors is None:
            continue

        for key in selectors:
            if key in podLabels:
                if podLabels[key] == selectors[key] :

                    for port in service["spec"]["ports"]:                        
                        exposures.append({
                                "serviceName": service["metadata"]["name"],
                                "port": port["port"],
                                "targetPort": port["target_port"],
                                "serviceType": service["spec"]["type"]
                            })

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning from /pods/exposure endpoint.",
        payLoad = exposures
    )
