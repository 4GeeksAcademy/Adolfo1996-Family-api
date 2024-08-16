"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if len(members) <= 0:
        return jsonify({'error':'members not found'}), 400
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member_returned = jackson_family.get_member(id)
    if member_returned: 
       return jsonify(member_returned), 200
    else:
        return jsonify({"message": "user not found"}), 200
    
@app.route('/member', methods=['POST'])
def NEW_MEMBER():
    request_body = request.json
    new_member = jackson_family.add_member(request_body)
    if new_member:
        return jsonify(new_member), 200
    else:
        return jsonify({'message': 'bad request'}), 400

@app.route( '/member/<int:id>' , methods=["DELETE"])
def erase_member(id):
    member_erased = jackson_family.delete_member(id)
    if member_erased: 
        return jsonify({'done':True}), 200
    else:
        return jsonify({'done':False}), 400
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
