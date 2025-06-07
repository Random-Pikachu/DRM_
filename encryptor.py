from PyPDF2 import PdfReader
from cryptography.fernet import Fernet
import os 
import json
import datetime

# No. of pages 
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
    
    wantEncrypt = input("Do you want to encrypt the file(y/n): ")

    print("\n")
    if (wantEncrypt == 'y'):
        email = input("Enter email of receiver: ")
        startTime = input("Enter start time [eg. 2025-06-07 16:10:56]: ")
        endTime = input("Active Timeperiod [default: 60 min]: ")
        outputPath = input("Enter the output path (output/metadata.json [default]): ")

        if not outputPath:
            outputPath = "output/metadata.json"

        createMetaData(email, startTime, endTime, fileName, outputPath)
        
        encryptedPDF = cipher.encrypt(reader)

        parentDir = os.path.dirname(outputPath)
        if not parentDir:
            parentDir = "output"

        os.makedirs(parentDir, exist_ok=True)
        with open(os.path.join(parentDir, f'{fileName}_{datetime.datetime.now().strftime('%H-%M-%S')}.pdf'), "wb") as f:
            f.write(encryptedPDF)

    
    return






def createMetaData(email: str, startTime: str, endTime: str, fileName: str, outputPath: str = "output/metdata.json"):
    '''
        Creates metadata JSON file containing access information of file.

        Args:
            email (str): Receiver's Email Address
            startTime (str): Start time of access period (e.g. "2025-06-07 16:10:56")
            endTime (str): End time of access period (e.g. "2025-06-07 17:10:56")
            fileName (str): The name of pdf file to be encrypted
            outputPath (str, optional): Path to store metadata.json
        
        Returns:
            none
    '''


    metadata = {
        "email":email,
        "allowed_ip": "", #will store in on first login
        "startTime": startTime,
        "endTime": endTime,
        "fileName": fileName
    }
    print(outputPath)

    parentDir = os.path.dirname(outputPath)
    if parentDir and not os.path.exists(parentDir):
        os.makedirs(parentDir, exist_ok=True)


    metadataObj = json.dumps(metadata, indent=4)
    with open(outputPath, "w") as f:
        f.write(metadataObj)

    return

encryptPDF()