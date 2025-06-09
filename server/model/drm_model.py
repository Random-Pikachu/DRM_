from config.connection import db
from datetime import datetime

class DRM_Mode:
    collection = db.db.drm_data

    @staticmethod
    def insertData(fileId, key, auth):
        return DRM_Mode.collection.insert_one({
            "fileId": fileId,
            "key" : key,
            "auth": auth,
            "ip": ""
        })
    
    @staticmethod
    def update_after_first_open(fileId, auth, ip):
        return DRM_Mode.collection.update_one({
            {"fileId": fileId, "auth": auth},
            {
                "$set" :{
                    "ip": ip
                }
            }
        })
    
    @staticmethod
    def getKey(fileId, auth, open):
        if (open == 1):
            doc = DRM_Mode.collection.find_one({
               "$and":[
                   {"fileId": fileId},
                   {"email": auth}
               ]
            })

            if doc:
                return doc["key"]
            
            return None

        doc = DRM_Mode.collection.find_one({
               "$and":[
                   {"fileId": fileId},
                   {"ip": auth}
               ] 
            })

        if doc:
            return doc["key"]