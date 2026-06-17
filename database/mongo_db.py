from pymongo import MongoClient
from config import Config

# MongoDB Connection
client = MongoClient(Config.MONGO_URI)

# Select Database
db = client[Config.MONGO_DATABASE]

# Collections
location_collection = db["location_history"]

geofence_collection = db["geofences"]

notification_collection = db["notification_logs"]

