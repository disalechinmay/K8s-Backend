from __main__ import app, v1, appsv1, client
from flask import jsonify, request
import json

# Usage: Returns a list of all services present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/servicesx', methods = ['GET'])
def getServices():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allServices = v1.list_namespaced_service(namespace).to_dict()

	returnList = []

	for service in allServices["items"]:
		tempDict = {}
		tempDict["serviceName"] = service["metadata"]["name"]
		tempDict["serviceType"] = service["spec"]["type"]
		tempDict["serviceLabels"] = service["metadata"]["labels"]
		tempDict["serviceAnnotations"] = service["metadata"]["annotations"]
		tempDict["serviceSelectors"] = service["spec"]["selector"]
		tempDict["servicePort"] = []
		tempDict["serviceTargetPort"] = []

		for port in service["spec"]["ports"]:
			tempDict["servicePort"].append(port["port"])
			tempDict["serviceTargetPort"].append(port["target_port"])

		returnList.append(tempDict)

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning a list of services of '" + namespace + "' namespace.",
		payLoad = returnList
	)

@app.route('/service', methods = ["GET"])
def getService():
	 # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    serviceName = request.args.get("serviceName")

    if (namespace is None) and (serviceName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & serviceName name is not specified as query params.",
            payLoad = None
        )

    if(namespace is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as query params.",
            payLoad = None
        )

    if(serviceName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Deployment name is not specified as query params.",
            payLoad = Non
        )

    service = v1.read_namespaced_service(namespace = namespace, name = serviceName).to_dict()

   

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning deployment '" + serviceName + "' of '" + namespace + "' namespace.",
        payLoad = service
    )

# Usage: Patches a service present in the specified namespace.
# Method: GET
# Params: namespace, serviceName
@app.route('/service', methods = ['PATCH'])
def patchservice():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()


        result = v1.patch_namespaced_service(
                namespace = requestJSON["namespace"],
                name = requestJSON["serviceName"],
                body = requestJSON["body"]
            )

        return jsonify(
            status = "SUCCESS",
            statusDetails = "service patched successfully.",
            payLoad = result.to_dict()
        )
        
    except Exception as e:
        return jsonify(
                status = "FAILURE",
                statusDetails = "service patch failed.",
                payLoad = json.loads(e.body) if e.body else str(e)
            )



# Usage: Creates a service in the specified namespace.
# Method: POST
# Body Params: namespace, serviceName, portMappings, targetDeployemnts, serviceType
@app.route('/service', methods = ['POST'])
def createService():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        selectors = {}

        for deployment in requestJSON["targetDeployments"]:

            deployment = appsv1.read_namespaced_deployment(namespace = requestJSON["namespace"], name = deployment).to_dict()
            
            for key, value in deployment["spec"]["selector"]["match_labels"].items():
                selectors[key] = value

        
        portMappings = []

        for mapping in requestJSON["portMappings"]:

            portMappings.append(client.V1ServicePort(
                    port = int(mapping["key"]),
                    target_port = int(mapping["value"])
                ))

        
        serviceSpec = client.V1ServiceSpec(
                    type = requestJSON["serviceType"],
                    selector = selectors,
                    ports = portMappings
                )

        serviceBody = client.V1Service(
                metadata = client.V1ObjectMeta(name = requestJSON["serviceName"]),
                spec = serviceSpec
            )

        retValue = v1.create_namespaced_service(namespace = requestJSON["namespace"], body = serviceBody).to_dict()

        return jsonify(
                status = "SUCCESS",
                statusDetails = "Service created successfully.",
                payLoad = None
            )

    except Exception as e:
        print(str(e))
        return jsonify(
                status = "FAILURE",
                statusDetails = "Service creation failed.",
                payLoad = json.loads(e.body)
            )



# Usage: Deletes a service by serviceName & namespace specified in request.
# Method: DELETE
# Request Body: JSON {
#                        serviceName: "",
#                        namespace: ""
#                    }
@app.route('/service', methods = ['DELETE'])
def deleteService():

    # Retrieve request's JSON object
    requestJSON = request.get_json()

    if (requestJSON["namespace"] is None) and (requestJSON["serviceName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & service name is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["namespace"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as body params.",
            payLoad = None
        )

    if(requestJSON["serviceName"] is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Service name is not specified as body params.",
            payLoad = None
        )


    returnValue = v1.delete_namespaced_service(
            requestJSON["serviceName"], requestJSON["namespace"]
        ).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Attempted to delete service '" + requestJSON["serviceName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
        payLoad = None
    )
