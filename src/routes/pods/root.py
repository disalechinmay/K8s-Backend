from __main__ import app, v1, client
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
        statusDetails = "Returning a list of pods in '" + namespace + "' namespace.",
        payLoad = returnList
    )


# Usage: Returns a pod present in the specified namespace.
# Method: GET
# Params: namespace, podName
@app.route('/pod', methods = ['GET'])
def getPod():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    podName = request.args.get("podName")

    if (namespace is None) and (podName is None):
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

    if(podName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Pod name is not specified as query params.",
            payLoad = None
        )

    pod = v1.read_namespaced_pod(namespace = namespace, name = podName).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning secret '" + podName + "' of '" + namespace + "' namespace.",
        payLoad = pod
    )


# Usage: Deletes a pod by podName & namespace specified in request.
# Method: DELETE
# Request Body: JSON {
#                        podName: "",
#                        namespace: ""
#                    }
@app.route('/pod', methods = ['DELETE'])
def deletePod():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    if (requestJSON["namespace"] is None) and (requestJSON["podName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & pod name is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["namespace"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["podName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Pod name is not specified as body params.",
            payLoad = None
        )


    returnValue = v1.delete_namespaced_pod(
            requestJSON["podName"], requestJSON["namespace"]
        ).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Attempted to delete pod '" + requestJSON["podName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
        payLoad = None
    )

# Usage: Returns list of exposures by podName & namespace specified in request.
# Method: GET
# Params: namespace, podName
@app.route('/pod/exposure', methods = ['GET'])
def getPodExposure():

    namespace = request.args.get("namespace")
    podName = request.args.get("podName")


    if (namespace is None) and (podName is None):
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

    if(podName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Pod name is not specified as query params.",
            payLoad = None
        )

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
        statusDetails = "Returning a list of exposures for pod '" + podName + "' of '" + namespace + "' namespace.",
        payLoad = exposures
    )


# Usage: Creates a pod in the specified namespace.
# Method: POST
# Body Params: namespace, podName, podImage, podVars
@app.route('/pod', methods = ['POST'])
def createPod():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        meta = client.V1ObjectMeta(name = requestJSON["podName"])

        envList = []
        for variableObj in requestJSON["podVars"] :

            keySel = client.V1ConfigMapKeySelector(
                    name = variableObj["configMapName"],
                    key = variableObj["variable"]
                )

            envVarSource = client.V1EnvVarSource(
                    config_map_key_ref = keySel
                )


            envVar = client.V1EnvVar(
                    name = variableObj["variable"],
                    value_from = envVarSource
                )

            envList.append(envVar)

        containerList = []
        container = client.V1Container(
                name = requestJSON["podName"],
                image = requestJSON["podImage"],
                env = envList
            )
        containerList.append(container)

        spec = client.V1PodSpec(
                containers = containerList
            )

        body = client.V1Pod(
                metadata = meta,
                spec = spec
            )

        response = v1.create_namespaced_pod(namespace = requestJSON["namespace"], body = body).to_dict()

        return jsonify(
                status = "SUCCESS",
                statusDetails = "Secret created successfully.",
                payLoad = None
            )

    except Exception as e:
        print(str(e))
        return jsonify(
                status = "FAILURE",
                statusDetails = "Secret creation failed.",
                payLoad = json.loads(e.body)
            )

