from flask import Flask
from config.connection import connectDb


app = Flask(__name__)





if __name__ == '__main__':
    connectDb(app)
    app.run(port=5600, debug = True)