from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def serveHomeGET():
    return "<h1>Backend is working</h1>"

@app.route("/", methods=['POST'])
def serveHomePOST():
    return "ok"



if __name__ == '__main__':
    app.run(port=5600, debug = True)