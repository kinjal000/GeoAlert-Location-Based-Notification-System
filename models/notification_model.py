from database.mongo_db import notification_collection

class NotificationModel:
    @staticmethod
    def save_notification(user_id, message_data):
        # Handle string message or rich dynamic dictionary
        if isinstance(message_data, dict):
            notification = {
                "user_id": int(user_id),
                "icon": message_data.get("icon", "🔔"),
                "title": message_data.get("title", "Alert"),
                "message": message_data.get("description", ""),
                "location": message_data.get("location", "Unknown Location"),
                "time": message_data.get("time", "Just Now"),
                "status": message_data.get("status", "Active"),
                "category": message_data.get("category", "General")
            }
        else:
            notification = {
                "user_id": int(user_id),
                "icon": "🔔",
                "title": "System Alert",
                "message": str(message_data),
                "location": "Monitored Point",
                "time": "Just Now",
                "status": "Active",
                "category": "General"
            }
        
        notification_collection.insert_one(notification)
        return True

    @staticmethod
    def get_notifications(user_id):
        # Query and reverse array order to ensure newest shows first
        notifications = list(notification_collection.find({"user_id": int(user_id)}, {"_id": 0}))
        notifications.reverse()
        return notifications

    @staticmethod
    def delete_notifications(user_id):
        notification_collection.delete_many({"user_id": int(user_id)})
        return True