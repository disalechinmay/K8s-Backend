from __main__ import app, v1, client
from flask import jsonify, request
import json


# Usage: Returns a list of all configmaps present in the specified namespace.
# Method: GET
# Params: namespace = "default"
@app.route('/configmaps', methods=['GET'])
def getConfigMaps():
    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    if namespace is None:
        namespace = "default"

    allConfigMaps = v1.list_namespaced_config_map(namespace).to_dict()

    returnList = []

    for configMap in allConfigMaps["items"]:
        tempDict = {}

        tempDict["configMapName"] = configMap["metadata"]["name"]
        tempDict["configMapData"] = configMap["data"]
        tempDict["configMapLabels"] = configMap["metadata"]["labels"]
        tempDict["configMapAnnotations"] = configMap["metadata"]["annotations"]

        returnList.append(tempDict)

    return jsonify(
        status="SUCCESS",
        statusDetails="Returning a list of config maps of '" + namespace + "' namespace.",
        payLoad=returnList
    )


# Usage: Returns a configMap present in the specified namespace.
# Method: GET
# Params: namespace, configMapName
@app.route('/configmap', methods=['GET'])
def getConfigMap():
    # Get query param "namespace", if not present set to "default"
    namespace = request.args.get("namespace")
    configMapName = request.args.get("configMapName")

    if (namespace is None) and (configMapName is None):
        return jsonify(
            status="FAILURE",
            statusDetails="Namespace & configMap name is not specified as query params.",
            payLoad=None
        )

    if (namespace is None):
        return jsonify(
            status="FAILURE",
            statusDetails="Namespace is not specified as query params.",
            payLoad=None
        )

    if (configMapName is None):
        return jsonify(
            status="FAILURE",
            statusDetails="ConfigMap name is not specified as query params.",
            payLoad=None
        )

    configMap = v1.read_namespaced_config_map(namespace=namespace, name=configMapName).to_dict()

    return jsonify(
        status="SUCCESS",
        statusDetails="Returning configMap '" + configMapName + "' of '" + namespace + "' namespace.",
        payLoad=configMap
    )


# Usage: Creates a configmap in the specified namespace.
# Method: POST
# Body Params: namespace, configMapName, configMapData
@app.route('/configmap', methods=['POST'])
def createConfigMap():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        data = {}
        for pair in requestJSON["configMapData"]:
            data[str(pair["key"])] = str(pair["value"])

        meta = client.V1ObjectMeta(name=requestJSON["configMapName"])
        body = client.V1ConfigMap(
            metadata=meta,
            data=data
        )

        response = v1.create_namespaced_config_map(namespace=requestJSON["namespace"], body=body).to_dict()

        return jsonify(
            status="SUCCESS",
            statusDetails="Config map created successfully.",
            payLoad=response
        )

    except Exception as e:
        print(str(e))
        return jsonify(
            status="FAILURE",
            statusDetails="Config map creation failed.",
            payLoad=json.loads(e.body)
        )


# Usage: Deletes a config map in the specified namespace.
# Method: DELETE
# Body Params: namespace, configMapName
@app.route('/configmap', methods=['DELETE'])
def deleteConfigMap():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        response = v1.delete_namespaced_config_map(namespace=requestJSON["namespace"],
                                                   name=requestJSON["configMapName"]).to_dict()

        return jsonify(
            status="SUCCESS",
            statusDetails="Deleting config map '" + requestJSON["configMapName"] + "' of '" + requestJSON[
                "namespace"] + "' namespace.",
            payLoad=response
        )

    except Exception as e:
        return jsonify(
            status="FAILURE",
            statusDetails="Config map deletion failed.",
            payLoad=json.loads(e.body)
        )


@app.route('/configmap', methods=['PATCH'])
def patchConfigMap():
    try:
        # Retrieve request's JSON object
        requestJSON = request.get_json()

        result = v1.patch_namespaced_config_map(
            namespace=requestJSON["namespace"],
            name=requestJSON["configMapName"],
            body=requestJSON["body"]
        )

        return jsonify(
            status="SUCCESS",
            statusDetails="ConfigMap patched successfully.",
            payLoad=result.to_dict()
        )

    except Exception as e:
        return jsonify(
            status="FAILURE",
            statusDetails="ConfigMap patch failed.",
            payLoad=str(e)
        )
