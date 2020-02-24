from __main__ import app, appsv1
from flask import jsonify, request
import json

# Usage: Returns a list of all deployments present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/deployments', methods = ['GET'])
def getDeployments():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    allDeployments = appsv1.list_namespaced_deployment(namespace).to_dict()

    returnList = []

    for deployment in allDeployments["items"]:
        tempDict = {}
        tempDict["deploymentName"] = deployment["metadata"]["name"]
        tempDict["deploymentLabels"] = deployment["metadata"]["labels"]
        tempDict["deploymentAnnotations"] = deployment["metadata"]["annotations"]
        tempDict["deploymentReplicas"] = deployment["spec"]["replicas"]
        tempDict["deploymentSelectors"] = {}

        # Clubbing all kinds of selectors into deploymentSelectors
        if deployment["spec"]["selector"]["match_expressions"]:
            for key, value in deployment["spec"]["selector"]["match_expressions"].items():
                tempDict["deploymentSelectors"][key] = value
        if deployment["spec"]["selector"]["match_labels"]:
            for key, value in deployment["spec"]["selector"]["match_labels"].items():
                tempDict["deploymentSelectors"][key] = value

        tempDict["deploymentTemplateLabels"] = {}
        if deployment["spec"]["template"]["metadata"]["labels"]:
            for key, value in deployment["spec"]["template"]["metadata"]["labels"].items():
                tempDict["deploymentTemplateLabels"][key] = value

        tempDict["deploymentTemplateContainers"] = []
        for container in deployment["spec"]["template"]["spec"]["containers"]:
            tempDict["deploymentTemplateContainers"].append(container["image"])

        returnList.append(tempDict)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning data from /deployments endpoint.",
        payLoad = returnList
    )


# Usage: Returns a list of all deployments present in the specified namespace.
# Method: GET
# Params: namespace, resourceName
@app.route('/deployment', methods = ['GET'])
def getDeployment():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    resourceName = request.args.get("resourceName")

    if (namespace is None) and (resourceName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & resource name is not specified as query params.",
            payLoad = returnList
        )

    if(namespace is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as query params.",
            payLoad = returnList
        )

    if(resourceName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Resource name is not specified as query params.",
            payLoad = returnList
        )

    deployment = appsv1.read_namespaced_deployment(namespace = namespace, name = resourceName).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning data from /deployment endpoint.",
        payLoad = deployment
    )

# Usage: Returns a list of all deployments present in the specified namespace.
# Method: GET
# Params: namespace, resourceName
@app.route('/deployment', methods = ['PATCH'])
def patchDeployment():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = appsv1.patch_namespaced_deployment(
                namespace = requestJSON["namespace"],
                name = requestJSON["resourceName"],
                body = requestJSON["body"]
            )

        return jsonify(
            status = "SUCCESS",
            statusDetails = "Deployment patched successfully.",
            payLoad = result.status.to_dict()
        )

    except Exception as e:
        return jsonify(
                status = "FAILURE",
                statusDetails = "Deployment patch failed.",
                payLoad = json.loads(e.body)
            )
