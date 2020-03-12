from __main__ import app, v1, client
from flask import jsonify, request
import json


# Usage: Returns a list of all namespaces setup in the cluster.
# Method: GET
# Params: None
@app.route('/namespaces', methods = ['GET'])
def getNamespaces():

    allNamespaces = v1.list_namespace().to_dict()

    # Putting all namespaces in a single list
    namespaceList = []
    for namespace in allNamespaces["items"]:
        namespaceList.append(namespace["metadata"]["name"])

    return jsonify(
        status = "SUCCESS",
        statusDetails = "Returning a list of namespaces present in the cluster.",
        payLoad = namespaceList
    )

@app.route('/namespace', methods = ['POST'])
def createNamespace():
    try:
        requestJSON = request.get_json()
        print(requestJSON)

        data = client.V1ObjectMeta(name =  requestJSON["namespace"] )

        body = client.V1Namespace(metadata = data)

        returnValue = v1.create_namespace(body = body).to_dict()

        return jsonify(
        status = "SUCCESS",
        statusDetails = "Created namespace successfully.",
        payLoad = returnValue
        )

    except Exception as e:
        print(e)
        return jsonify(
                status = "FAILURE",
                statusDetails = "Namespace creation failed.",
                payLoad = json.loads(e.body)
            )


@app.route('/namespace', methods = ['DELETE'])
def deleteNamespace():
    try:
        requestJSON = request.get_json()

        returnValue = v1.delete_namespace(name = requestJSON["namespace"]).to_dict()

        return jsonify(
        status = "SUCCESS",
        statusDetails = "Namespace deleted successfully.",
        payLoad = returnValue
        )

    except Exception as e:
        return jsonify(
                status = "FAILURE",
                statusDetails = "Namespace deletion failed.",
                payLoad = json.loads(e.body)
            )



