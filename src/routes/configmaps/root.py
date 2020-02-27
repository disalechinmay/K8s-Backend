from __main__ import app, v1
from flask import jsonify, request
import json

# Usage: Returns a list of all configmaps present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/configmaps', methods = ['GET'])
def getConfigMaps():

# Get query param "namespace", if not present set to "default"

	namespace = request.args.get("namespace")
	if namespace is None:
		namespace = "default"

	allConfigMaps = v1.list_namespaced_config_map(namespace).to_dict()

	returnList = []

	for configMap in allConfigMaps["items"]:
		tempDict={}
		tempDict["configMapName"] = configMap["metadata"]["name"]
		tempDict["configMapData"]=configMap["data"]

		tempDict["configMapLabels"] = configMap["metadata"]["labels"]
		tempDict["configMapAnnotations"] = configMap["metadata"]["annotations"]

		returnList.append(tempDict)


	return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning data from /configMaps endpoint.",
        payLoad = returnList
    )



# @app.route('/configmaps', methods = ['PATCH'])
# def patchConfigMap():
#     try: 
#         # Retrieve request's JSON object
#         requestJSON = request.get_json()

#         result = v1.patch_namespaced_config_map(
#                 namespace = requestJSON["namespace"],
#                 name = requestJSON["resourceName"],
#                 body = requestJSON["body"]
#             )

#         return jsonify(
#             status = "SUCCESS",
#             statusDetails = "Deployment patched successfully.",
#             payLoad = result.status.to_dict()
#         )
        
#     except Exception as e:
#         return jsonify(
#                 status = "FAILURE",
#                 statusDetails = "Deployment patch failed.",
#                 payLoad = json.loads(e.body)
#             )
