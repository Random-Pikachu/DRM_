from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

db = PyMongo()
load_dotenv()


def connectDb(app):
    """Initialize connection with mongo database
    
    Keyword arguments:
    app -- instance of flask app
    Return: None
    """
    try:
        app.config["MONGO_URI"] = os.getenv("MONGO_URI")
        print("[✓] MongoDB connected successfully")
        db.init_app(app)

    except Exception as e:
        print(f"[✗] MongoDB connection failed: {e}")