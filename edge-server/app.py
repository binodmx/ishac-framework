import util
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "200 OK"

@app.route("/validate", methods=['POST'])
def validate():
    return jsonify(util.validate(request.get_json()))
