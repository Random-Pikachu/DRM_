from PyPDF2 import PdfReader
from cryptography.fernet import Fernet
import os 
import json
import datetime
import uuid
import zipfile


APP_SECRET = b'QF_uqnUuQISVwIt60COjcJoj8se95orGMJPbxmmk6qY=' # a global key for accessing the key.bin

def encryptPDF():
    """
    Encrypts a PDF file specified by the user and creates associated metadata.
    
    Args:
        None
    
    Returns:
        None
    """

    fileNameDir = input("Enter the path of pdf file: ")
    fileName = os.path.basename(fileNameDir)

    key = Fernet.generate_key()
    cipher = Fernet(key)

    with open(fileNameDir, "rb") as f:
        reader = f.read()
    
    wantEncrypt = input("Do you want to encrypt the file(y/n): ").lower()

    print("\n")
    if (wantEncrypt != 'y'):
        print("Process aborted !")
        return
    

    email = input("Enter email of receiver: ")
    startTime = input("Enter start time [eg. 2025-06-07 16:10:56]: ")
    endTime = input("End time: ")
    outputPath = input("Enter the output path (optional): ")

    

    #encrypting the pdf
    encryptedPDF = cipher.encrypt(reader)

    parentDir = os.path.dirname(outputPath)
    if not parentDir:
        parentDir = "output"
    temp = os.path.join(parentDir, f"{fileName[:-4]}_{datetime.datetime.now().strftime('%H-%M-%S')}")
    os.makedirs(temp, exist_ok=True)

    if not outputPath:
        outputPath = temp
    
    with open(os.path.join(temp, f'{fileName}_{datetime.datetime.now().strftime('%H-%M-%S')}.pdf'), "wb") as f:
        f.write(encryptedPDF)


    #writing metadata
    createMetaData(email, startTime, endTime, fileName, outputPath)

    #saving key.bin
    app_cipher = Fernet(APP_SECRET)
    encryptedKey = app_cipher.encrypt(key)

    with open(os.path.join(temp, "key.bin"), "wb") as kf:
        kf.write(encryptedKey)

    #creating drm package
    parent_of_output = os.path.dirname(outputPath)
    createDRMPackage(temp, f'{parent_of_output}/{fileName}_{datetime.datetime.now().strftime('%H-%M-%S')}.drm')

    
    return






def createMetaData(email: str, startTime: str, endTime: str, fileName: str, outputPath: str = "output/metdata.json"):

    fileId = uuid.uuid4()

    metadata = {
        "email":email,
        "allowed_ip": "", #will store in on first login
        "startTime": startTime,
        "endTime": endTime,
        "fileName": fileName,
        "fileId": str(fileId),
        "lastUpdated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open": 1
    }
    
    print(outputPath)

    parentDir = os.path.dirname(outputPath)
    if parentDir and not os.path.exists(parentDir):
        os.makedirs(parentDir, exist_ok=True)


    metadataObj = json.dumps(metadata, indent=4)
    with open(os.path.join(outputPath, "metadata.json"), "w") as f:
        f.write(metadataObj)

    return



def createDRMPackage(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w',zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname)



encryptPDF()