from __main__ import app
from flask import jsonify

@app.route('/pods/test', methods=['GET'])
def test():
    return jsonify(
    	status = "SUCCESS",
    	statusDetails = "Returning data from /pods/test endpoint.",
    	payLoad = "Testing /pods/test endpoint."
    	)
