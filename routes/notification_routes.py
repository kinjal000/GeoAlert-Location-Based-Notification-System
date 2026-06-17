from flask import Blueprint, request
from controllers.notification_controller import NotificationController

# Create Blueprint
notification_bp = Blueprint("notification_bp", __name__)

# ---------------------------------------
# Get User Notifications
# URL : GET /notifications/<user_id>
# ---------------------------------------

@notification_bp.route("/notifications/<int:user_id>", methods=["GET"])
def get_notifications(user_id):

    return NotificationController.get_notifications(user_id)


# ---------------------------------------
# Send Notification
# URL : POST /send-notification
# ---------------------------------------

@notification_bp.route("/send-notification", methods=["POST"])
def send_notification():

    data = request.get_json()

    user_id = data.get("user_id")

    message = data.get("message")

    return NotificationController.send_notification(
        user_id,
        message
    )