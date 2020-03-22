from __main__ import app, appsv1, client
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
        tempDict["deploymentReadyReplicas"] = deployment["status"]["ready_replicas"]
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
        statusDetails = "Returning a list of deployments in '" + namespace + "' namespace.",
        payLoad = returnList
    )


# Usage: Returns a deployment present in the specified namespace.
# Method: GET
# Params: namespace, deploymentName
@app.route('/deployment', methods = ['GET'])
def getDeployment():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    deploymentName = request.args.get("deploymentName")

    if (namespace is None) and (deploymentName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & deployment name is not specified as query params.",
            payLoad = None
        )

    if(namespace is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as query params.",
            payLoad = None
        )

    if(deploymentName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Deployment name is not specified as query params.",
            payLoad = None
        )

    deployment = appsv1.read_namespaced_deployment(namespace = namespace, name = deploymentName).to_dict()

    for container in deployment["spec"]["template"]["spec"]["containers"]:
        for port in container["ports"]:
            port["containerPort"] = port["container_port"]
            del port["container_port"]
            print(port)

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning deployment '" + deploymentName + "' of '" + namespace + "' namespace.",
        payLoad = deployment
    )

# Usage: Returns a list of all deployments present in the specified namespace.
# Method: GET
# Params: namespace, deploymentName
@app.route('/deployment', methods = ['PATCH'])
def patchDeployment():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = appsv1.patch_namespaced_deployment(
                namespace = requestJSON["namespace"],
                name = requestJSON["deploymentName"],
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


# Usage: Creates a deployment in the specified namespace.
# Method: POST
# Body Params: namespace, deploymentName, deploymentImage, deploymentReplicas, deploymentVars
@app.route('/deployment', methods = ['POST'])
def createDeployment():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        meta = client.V1ObjectMeta(name = requestJSON["deploymentName"])

        envList = []
        for variableObj in requestJSON["deploymentVars"] :

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
                name = requestJSON["deploymentName"],
                image = requestJSON["deploymentImage"],
                env = envList
            )
        containerList.append(container)

        podSpec = client.V1PodSpec(
                containers = containerList
            )

        podTemplateSpec = client.V1PodTemplateSpec(
                spec = podSpec,
                metadata = client.V1ObjectMeta(labels = {"app": requestJSON["deploymentName"]})
            )

        # selector = client.V1LabelSelector(match_labels = {"app": requestJSON["deploymentName"]})

        spec = client.V1DeploymentSpec(
                replicas = int(requestJSON["deploymentReplicas"]),
                template = podTemplateSpec,                
                selector = selector
            )

        body = client.V1Deployment(
                metadata = meta,
                spec = spec
            )

        response = appsv1.create_namespaced_deployment(namespace = requestJSON["namespace"], body = body).to_dict()

        return jsonify(
                status = "SUCCESS",
                statusDetails = "Deployment created successfully.",
                payLoad = None
            )

    except Exception as e:
        print(str(e))
        return jsonify(
                status = "FAILURE",
                statusDetails = "Deployment creation failed.",
                payLoad = json.loads(e.body)
            )



# Usage: Deletes a deployment by deploymentName & namespace specified in request.
# Method: DELETE
# Request Body: JSON {
#                        deploymentName: "",
#                        namespace: ""
#                    }
@app.route('/deployment', methods = ['DELETE'])
def deleteDeployment():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    if (requestJSON["namespace"] is None) and (requestJSON["deploymentName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & deployment name is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["namespace"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["deploymentName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Deployment name is not specified as body params.",
            payLoad = None
        )


    returnValue = appsv1.delete_namespaced_deployment(
            requestJSON["deploymentName"], requestJSON["namespace"]
        ).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Attempted to delete deployment '" + requestJSON["deploymentName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
        payLoad = None
    )
