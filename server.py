# Read APIRef.txt before working on this repo.

from flask import Flask, jsonify

app = Flask(__name__)
from src.routes.pods import pods

@app.route('/test')
def testRoute():
    return jsonify(
    	status = "SUCCESS",
    	statusDetails = "Returning data from /test endpoint.",
    	payLoad = "Testing /test endpoint."
    	)

@app.errorhandler(404)
def pageNotFound(e):
	return jsonify(
		status = "FAILURE", 
		statusDetails = "You have reached an invalid endpoint.",
		payLoad = None
		)

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)
