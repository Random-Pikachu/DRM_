<h1 align="center" id="title">SecurePDF </h1>
<p style = "font-size:16px; ">A standalone offline <strong>Digital Rights Management (DRM)</strong> desktop application built using Python, CustomTkinter, and AES encryption. This tool allows secure sharing and controlled viewing of PDF documents, with features to restrict printing, copying, and unauthorized access.</p>

<h2>💻 Tech Stack</h2>

*   Python
*   CustomTkinter
*   PyMuPDF (fitz)
*   Cryptography


<h2>📁 Folder Structure </h2>

```bash
DRM
├── .gitignore
├── Readme.md
├── appfile
│   ├── app.py      #Main entry point
│   ├── decryptor.py #File: Decryption Logic
│   ├── decryptorView.py #GUI for file decryption window
│   ├── encryptor.py    #File: Encryption Logic
│   ├── senderView.py   #GUI for encryption window
│   ├── viewer.py   #GUI window for PDF Viewer
├── requirements.txt
```

<h2>⚒ How it Works</h2>

*   Admin encrypts the PDF and embeds metadata (Password, Access Time)
*   The application return a `.drm` package.
*   When the recipient opens the `.drm` file using the application:
    - On the first open, the user is prompted for a password.
    - Upon successful authentication, the device's MAC address is registered.
    - For all future accesses, the app verifies the MAC address and access time before opening the file.


<h2>🛡️ Features</h2>

*   Offline DRM enforcement
*   AES Based PDF Encryption
*   File access restricted to assigned MAC Address and assigned time period
*   Builtin PDF Viewer
    - Avoids Text Copy
    - Avoid Content Printing


<h2>🚀 Getting Started</h2>

<h3>🎯 Prerequisites</h3>
    1. Python
    <br>
    2. Virtual Enviroment (optional but required)

<h3>📩 Installation</h3>
<h4>1. Clone the repository</h4>

```bash
git clone https://github.com/zorro1107/DRM.git
cd DRM
```


<h4>2. Create Virtual Enviroment</h4>

```bash
python -m venv .env

#Activate (Windows)
.env\Scripts\activate

#Activate (MacOS/Linux)
source .env/bin/activate
```


<h4>3. Install Libraries</h4>

```bash
pip install -r requirements.txt
```

<h4>4. Run the files</h3>

```bash
cd appfile
python app.py
```

<h5 align="center" >Made with ❤</h5>
