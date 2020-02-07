from __main__ import app
from flask import jsonify
import array as arr
from kubernetes import client, config, kubernetes

config.load_kube_config()

v1 = client.CoreV1Api()

@app.route('/pods/test', methods=['GET'])
def test():
	print("Listing pods with their IPs:")
	api_response = (v1.read_namespaced_pod("reactapp-deployment-7fd5bc997-mdbpb", "default"))
	print(api_response.spec.containers[0].image)
	value={'pod_name' : api_response.metadata.name,
		   'Image_name':api_response.spec.containers[0].image,
			'labels': api_response.metadata.labels
		   }
			# "labels+"+api_response.metadata.labels[0],
			# "Image_name"+api_response.spec.containers[0].image]
	return jsonify(
    	status = "SUCCESS",
    	statusDetails = "Returning data from /pods/test endpoint.",
    	payLoad = value
    	)
