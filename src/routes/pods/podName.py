# from __main__ import app
# from __main__ import v1
# from flask import jsonify, request
# import json

# @app.route('/pod/<podname>', methods=['GET'])
# def isExposed():
#     namespace = request.args.get("namespace")
# 	if namespace is None:
#         namespace = "default"

# 	allPods = v1.list_namespaced_pod(namespace).to_dict()
#     allServices = v1.list_namespaced_service(namespace).to_dict()

#     for pod in allPods["items"]:
# 		tempDict = {}
# 		tempDict["podLabels"] = pod["metadata"]["labels"]

   



#     # return jsonify(
# 	# 	isExposed = 

# 	# 	port = "Returning data from /services/ endpoint.",
# 	# 	targetPort = 
# 	# 	)
