from flask import Flask
from config.connection import connectDb
from routes.routes import router

app = Flask(__name__)
app.register_blueprint(router)

@app.route('/', methods= ['GET'])
def serveHome():
    return "Backend is running!"


if __name__ == '__main__':
    connectDb(app)
    app.run(port=5600, debug = True)