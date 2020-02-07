from __main__ import app
from __main__ import v1
from flask import jsonify
import json

@app.route('/nodes/', methods=['GET'])
def getNodes():

	allNodes = v1.list_node().to_dict()

	return jsonify(
		status = "SUCCESS",
		statusDetails = "Returning data from /nodes/ endpoint.",
		payLoad = allNodes
		)
