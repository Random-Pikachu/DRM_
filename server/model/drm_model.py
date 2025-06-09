from config.connection import db
from datetime import datetime

class DRM_Mode:

    @staticmethod
    def insertData(fileId, key, auth):
        collection = db.db.drm_data

        return collection.insert_one({
            "fileId": fileId,
            "key" : key,
            "auth": auth,
            "ip": ""
        })
    
    @staticmethod
    def update_after_first_open(fileId, auth, ip):
        collection = db.db.drm_data

        return collection.update_one(
            {"fileId": fileId, "auth": auth},
            {"$set": {"ip": ip}}
        )
    
    @staticmethod
    def getKey(fileId, auth, open):
        collection = db.db.drm_data

        if (open == 1):
            doc = collection.find_one({
               "$and":[
                   {"fileId": fileId},
                   {"auth": auth}
               ]
            })

            if doc:
                return doc["key"]
            
            return None

        doc = collection.find_one({
               "$and":[
                   {"fileId": fileId},
                   {"ip": auth}
               ] 
            })

        if doc:
            return doc["key"]
        
        return None