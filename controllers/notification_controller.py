from flask import jsonify
from services.notification_service import NotificationService


class NotificationController:

    @staticmethod
    def get_notifications(user_id):

        try:

            notifications = NotificationService.get_user_notifications(
                user_id
            )

            return jsonify({
                "status": True,
                "data": notifications
            }), 200

        except Exception as e:

            return jsonify({
                "status": False,
                "message": str(e)
            }), 500

    @staticmethod
    def send_notification(user_id, message):

        try:

            result = NotificationService.send_notification(
                user_id,
                message
            )

            return jsonify(result), 200

        except Exception as e:

            return jsonify({
                "status": False,
                "message": str(e)
            }), 500