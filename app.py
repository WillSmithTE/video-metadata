import logging
import DataService
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({'message': 'heeeey'})

@app.route("/api/metadata", methods=["GET"])
def getMetadata():
    url = request.args.get('url')
    logging.info("getMetadata (url=%s)", url)
    return jsonify(DataService.getMetadata(url))

if os.environ.get("LOCAL") == "True":
    logging.debug("In local mode, starting server")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
