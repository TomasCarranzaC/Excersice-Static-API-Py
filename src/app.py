"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    all_members = jackson_family.get_all_members()
    return jsonify(all_members), 200

@app.route('/member', methods = ['POST'])
def add_member():
    new_member = request.get_json(force=True)
    jackson_family.add_member(new_member)
    return jsonify({}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    ex_member = jackson_family.delete_member(id)
    return jsonify({"done":True}), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id) :
    member = jackson_family.get_member(id)
    return jsonify(member), 200
    
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)