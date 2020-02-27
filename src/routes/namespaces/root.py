from __main__ import app, v1
from flask import jsonify
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
