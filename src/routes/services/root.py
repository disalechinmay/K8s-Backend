from __main__ import app, v1
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
