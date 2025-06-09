from flask import Blueprint, request, jsonify
from cerberus import Validator
from model.schema import key_schema
from model.drm_model import DRM_Mode


router = Blueprint("router", __name__)
validator = Validator(key_schema)

@router.route('/encryptionKey', methods = ['POST'])
def sendKey():
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    data = request.json
    if not validator.validate(data):
        return jsonify({"error": f"Data not in correct format \n {validator.errors}"}), 400
    
    DRM_Mode.insertData(
        fileId=data["fileId"],
        key=data["key"],
        auth=data["email"]
    )
    
    return jsonify({'message': "Data saved"}), 201


@router.route('/getKey', methods = ['POST'])
def getKey():
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    data = request.json
    if data["open"] == 1:
        DRM_Mode.update_after_first_open(
            fileId=data["fileId"],
            auth=data["email"],
            ip=data["ip"]
        )
    
    key = DRM_Mode.getKey(
        fileId=data["fileId"],
        open=data["open"],
        auth=data["email"] if data["open"] == 1 else data["ip"]
    )

    if key:
        return jsonify({"result": "Key extracted"}), 201
    
    return jsonify({"error": "key not found"}), 404