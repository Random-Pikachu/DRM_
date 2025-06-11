import socket
import os
from cryptography.fernet import Fernet
import tempfile
import zipfile
import json
from datetime import datetime
import viewer
import shutil

APP_SECRET = b'QF_uqnUuQISVwIt60COjcJoj8se95orGMJPbxmmk6qY=' # a global key for accessing the key.bin



def getIP():
    hostName = socket.gethostname()
    return socket.gethostbyname(hostName)

def extractDRM(drm_path):
    tempDir = tempfile.mkdtemp()
    with zipfile.ZipFile(drm_path, 'r') as zf:
        zf.extractall(tempDir)
    
    return tempDir


def loadMetadata(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def isAccessAllowd(metadata):
    currentTime = datetime.now()
    startTime = datetime.strptime(metadata["startTime"], "%Y-%m-%d %H:%M:%S")
    endTime = datetime.strptime(metadata["endTime"], "%Y-%m-%d %H:%M:%S")
    lastUpdated = datetime.strptime(metadata["lastUpdated"], "%Y-%m-%d %H:%M:%S")
    currentIp = getIP()
    

    if not (startTime<=currentTime<=endTime and currentTime>=lastUpdated):
        return False
    
    if metadata["allowed_ip"] and metadata["allowed_ip"] != currentIp:
        return False
    
    return True

def decryptKey(key_path):
    with open(key_path, 'rb') as f:
        encrypKey = f.read()
    
    return Fernet(APP_SECRET).decrypt(encrypKey)

def decryptPDF(file_path, key):
    with open(file_path, 'rb') as f:
        encrpyted_data = f.read()
    
    return Fernet(key).decrypt(encrpyted_data)

def saveMetadata(path, metadata):
    with open(path, 'w') as f:
        json.dump(metadata, f, indent=4)

def updateZipWithMetadata(drm_path, metadata_path):
    with open(metadata_path, 'r') as f:
        updated_metadata = f.read()

    with zipfile.ZipFile(drm_path, 'r') as zin:
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".drm")
        with zipfile.ZipFile(temp_zip.name, 'w') as zout:
            for item in zin.infolist():
                if item.filename == "metadata.json":
                    zout.writestr("metadata.json", updated_metadata)
                else:
                    zout.writestr(item.filename, zin.read(item.filename))
    shutil.move(temp_zip.name, drm_path)



def firstTime(metadata_path, metadata):
    if metadata["open"] == 1:
        input_email = input("enter the email: ")
        if input_email == metadata["email"]:
            metadata["allowed_ip"] = getIP()
            metadata["open"] = 0
            metadata["lastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            saveMetadata(metadata_path, metadata)
            print("First-time setup complete. Access granted.")
            return metadata
        
        else:
            print("Failed auth")
            return None
    
    return metadata
    
    

def viewPDFBytes(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf_path = temp_pdf.name
    
    viewer.launchViewer(temp_pdf_path)

def main(drm_path):
    #drm_path = input("Enter the path of .drm file: ")
    if not (os.path.exists(drm_path)):
        print("Provided path doesn't exist!")
        return


    tempDir = extractDRM(drm_path=drm_path)
    try:
        metadata_path = os.path.join(tempDir, "metadata.json")
        key_path = os.path.join(tempDir, "key.bin")
        pdf_path =None

        for f in os.listdir(tempDir):
            if f.endswith(".pdf"):
                pdf_path = os.path.join(tempDir, f)
                break
        
        if not all([os.path.exists(metadata_path), os.path.exists(key_path), os.path.exists(pdf_path)]):
            print("Invalid DRM package")
            return
        
        metadata= loadMetadata(metadata_path)

        
        if metadata["allowed_ip"] == "":
            metadata = firstTime(metadata_path, metadata)
            if metadata is None:
                return
        
        if not isAccessAllowd(metadata):
            print("IP Access restricted")
            return 
        

        print("File Opened!")
        pdf_key = decryptKey(key_path)
        decryptPDF_bytes = decryptPDF(pdf_path, pdf_key)

        viewPDFBytes(decryptPDF_bytes)
        updateZipWithMetadata(drm_path, metadata_path)

    except Exception as e:
        print("error: ", e)
    
    finally:
        shutil.rmtree(tempDir)
if __name__ == "__main__":
    main()