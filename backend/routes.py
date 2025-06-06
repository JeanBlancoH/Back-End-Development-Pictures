from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """returns all the pictures"""
    if data:
        return jsonify(data),200
    
    return {"message": "Server cannot find the requested resource."}, 404


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """returns a picture if the ID is specified"""
    if data:
        for x in data:
            if x['id'] == id:
                return jsonify(x), 200
    
    return {"message": "Server cannot find the requested resource."}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """extract the picture and append it to the dict"""
    picture = request.get_json()
    if picture in data:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    data.append(dict(picture))
    return jsonify(dict(id=picture['id'])), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """extract the picture and update it if the picture exists"""
    pic = request.get_json()
    for x in data:
        if x['id'] == id:
            data[data.index(x)] = pic
            return jsonify(x), 200
    
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """extract the pic ID and delete the picture if it exists"""
    for pic in data:
        if pic['id'] == id:
            data.remove(pic)
            return {}, 204

    return {"message": "picture not found"}, 404
