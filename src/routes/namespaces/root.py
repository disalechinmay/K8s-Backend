from __main__ import app
from __main__ import v1
from flask import jsonify
import json

@app.route('/namespaces/', methods=['GET'])
def getNamespaces():

	allNamespaces = v1.list_namespace().to_dict()

	# Putting all namespaces in a single list
	namespaceList = []
	for namespace in allNamespaces["items"]:
		namespaceList.append(namespace["metadata"]["name"])

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /namespaces/ endpoint.",
		payLoad = namespaceList
		)