from __main__ import app, v1, client
from flask import jsonify, request
import json

# Usage: Returns a list of all secrets present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/secrets', methods = ['GET'])
def getSecrets():

	# Get query param "namespace", if not present set to "default"
	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allSecrets = v1.list_namespaced_secret(namespace).to_dict()

	returnList = []

	for secret in allSecrets["items"]:
		tempDict={}
		tempDict["secretName"] = secret["metadata"]["name"]
		tempDict["secretData"] = secret["data"]
		tempDict["secretLabels"] = secret["metadata"]["labels"]
		tempDict["secretAnnotations"] = secret["metadata"]["annotations"]

		returnList.append(tempDict)


	return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning a list of secrets of '" + namespace + "' namespace.",
        payLoad = returnList
    )

# Usage: Returns a secret present in the specified namespace.
# Method: GET
# Params: namespace, secretName
@app.route('/secret', methods = ['GET'])
def getSecret():

    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")    
    secretName = request.args.get("secretName")

    if (namespace is None) and (secretName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace & secret name is not specified as query params.",
            payLoad = None
        )

    if(namespace is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Namespace is not specified as query params.",
            payLoad = None
        )

    if(secretName is None):
        return jsonify(
            status = "FAILURE",
            statusDetails = "Secret name is not specified as query params.",
            payLoad = None
        )

    secret = v1.read_namespaced_secret(namespace = namespace, name = secretName).to_dict()

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning secret '" + secretName + "' of '" + namespace + "' namespace.",
        payLoad = secret
    )

# Usage: Returns a list of all secrets present in the specified namespace.
# Method: GET
# Params: namespace, secretName
@app.route('/secret', methods = ['PATCH'])
def patchsecret():
    try: 
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = v1.patch_namespaced_secret(
                namespace = requestJSON["namespace"],
                name = requestJSON["secretName"],
                body = requestJSON["body"]
            )

        return jsonify(
            status = "SUCCESS",
            statusDetails = "Secret patched successfully.",
            payLoad = result.to_dict()
        )
        
    except Exception as e:
        return jsonify(
                status = "FAILURE",
                statusDetails = "Secret patch failed.",
                payLoad = str(e)
            )

# Usage: Creates a secret in the specified namespace.
# Method: POST
# Body Params: namespace, secretName, secretData
@app.route('/secret', methods = ['POST'])
def createSecret():
	try:
		# Retrieve request's JSON object
		requestJSON = request.get_json()

		data = {}
		for pair in requestJSON["secretData"]:
			data[str(pair["key"])] = str(pair["value"])

		print(data)

		meta = client.V1ObjectMeta(name = requestJSON["secretName"])
		body = client.V1Secret(
				metadata = meta,
				string_data = data
			)

		response = v1.create_namespaced_secret(namespace = requestJSON["namespace"], body = body).to_dict()

		return jsonify(
				status = "SUCCESS",
				statusDetails = "Secret created successfully.",
				payLoad = response
			)

	except Exception as e:
		return jsonify(
                status = "FAILURE",
                statusDetails = "Secret creation failed.",
                payLoad = json.loads(e.body)
            )


# Usage: Deletes a secret in the specified namespace.
# Method: DELETE
# Body Params: namespace, secretName
@app.route('/secret', methods = ['DELETE'])
def deleteSecret():
	try:
	    # Retrieve request's JSON object
	    requestJSON = request.get_json()

	    response = v1.delete_namespaced_secret(namespace = requestJSON["namespace"], name = requestJSON["secretName"]).to_dict()

	    return jsonify(
	        status = "SUCCESS",
	        statusDetails = "Deleting secret '" + requestJSON["secretName"] + "' of '" + requestJSON["namespace"] + "' namespace.",
	        payLoad = response
	    )

	except Exception as e:
		print(str(e))
