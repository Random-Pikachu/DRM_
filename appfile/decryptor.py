import socket
import os
from cryptography.fernet import Fernet
import tempfile
import zipfile
import json
from datetime import datetime
import viewer as viewer
import shutil
from getmac import get_mac_address

APP_SECRET = b'QF_uqnUuQISVwIt60COjcJoj8se95orGMJPbxmmk6qY=' # a global key for accessing the key.bin



def getIP():
    # hostName = socket.gethostname()
    # return socket.gethostbyname(hostName)
    return get_mac_address()

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
    
    temp_zip_path = tempfile.NamedTemporaryFile(delete=False, suffix=".drm").name

    with zipfile.ZipFile(drm_path, 'r') as zin, zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zout:
         for item in zin.infolist():
            if item.filename == "metadata.json":
                zout.writestr("metadata.json", updated_metadata)
            else:
                zout.writestr(item.filename, zin.read(item.filename))
    
    os.remove(drm_path)
    shutil.move(temp_zip_path, drm_path)



def firstTime(metadata_path, metadata, ask_pass):
    if metadata["open"] == 1:
        # input_email = input("enter the email: ")
        input_email = ask_pass()

        if input_email == metadata["password"]:
            metadata["allowed_ip"] = getIP()
            metadata["open"] = 0
            metadata["lastUpdated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            saveMetadata(metadata_path, metadata)
            # print("First-time setup complete. Access granted.")
            return metadata
        
        else:
            raise ValueError("Failed auth")
            return None
    
    return metadata
    
    

def viewPDFBytes(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf_path = temp_pdf.name
    
    viewer.launchViewer(temp_pdf_path)

def decrypt_drm_file(drm_path, ask_pass):
    # drm_path = input("Enter the path of .drm file: ")
    if not (os.path.exists(drm_path)):
        # print("Provided path doesn't exist!")
        # return
        raise FileNotFoundError("Provided path doesn't exist!")


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
            # print("Invalid DRM package")
            # return
            raise ValueError("Invalid DRM Package")
        
        metadata= loadMetadata(metadata_path)

        
        if metadata["allowed_ip"] == "":
            metadata = firstTime(metadata_path, metadata, ask_pass)
            if metadata is None:
                raise PermissionError("Password Authenthication Failed!")
        
        if not isAccessAllowd(metadata):
            # print("IP Access restricted")
            # return 
            raise PermissionError("MAC Address mismatch")        

        # print("File Opened!")
        pdf_key = decryptKey(key_path)
        decryptPDF_bytes = decryptPDF(pdf_path, pdf_key)

        viewPDFBytes(decryptPDF_bytes)
        updateZipWithMetadata(drm_path, metadata_path)

    except Exception as e:
        raise RuntimeError("error: ", e)
    
    finally:
        shutil.rmtree(tempDir)

# main()