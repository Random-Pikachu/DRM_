from PyPDF2 import PdfReader
from cryptography.fernet import Fernet
import os
import json
import datetime
import uuid
import zipfile

APP_SECRET = b'QF_uqnUuQISVwIt60COjcJoj8se95orGMJPbxmmk6qY='  # Global secret used to encrypt the encryption key

def encryptPDF(pdf_path: str, metadata: dict):
    """
    Encrypts a PDF file and generates metadata, key, and DRM package.

    Args:
        pdf_path (str): Path to the original PDF file.
        metadata (dict): Metadata information such as email, startTime, endTime, allowed_ip.

    Returns:
        output_drm_path (str): Path to the final .drm file created.
    """

    file_name = os.path.basename(pdf_path)
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Read and encrypt PDF
    with open(pdf_path, "rb") as f:
        original_pdf_data = f.read()
    encrypted_pdf_data = cipher.encrypt(original_pdf_data)

    # Setup output directory
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_base = os.path.join("output", f"{file_name[:-4]}_{timestamp}")
    os.makedirs(output_base, exist_ok=True)

    encrypted_pdf_path = os.path.join(output_base, f"{file_name}")
    with open(encrypted_pdf_path, "wb") as f:
        f.write(encrypted_pdf_data)

    # Save metadata
    save_metadata(metadata, file_name, output_base)

    # Encrypt and save the key
    encrypted_key = Fernet(APP_SECRET).encrypt(key)
    with open(os.path.join(output_base, "key.bin"), "wb") as f:
        f.write(encrypted_key)

    # Create final .drm package (ZIP)
    output_drm_path = os.path.join("output", f"{file_name[:-4]}_{timestamp}.drm")
    createDRMPackage(output_base, output_drm_path)

    return output_drm_path

def save_metadata(metadata: dict, file_name: str, output_folder: str):
    """
    Saves metadata as metadata.json in the given folder.
    """
    metadata["fileName"] = file_name
    metadata["fileId"] = str(uuid.uuid4())
    metadata["lastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata["open"] = 1

    with open(os.path.join(output_folder, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)

def createDRMPackage(folder_path, output_path):
    """
    Zips all contents of a folder into a .drm file (ZIP format).
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zf.write(full_path, arcname)

if __name__ == "__main__":
    encryptPDF()