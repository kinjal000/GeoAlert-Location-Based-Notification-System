from models.notification_model import NotificationModel


class NotificationService:

    @staticmethod
    def send_notification(user_id, message):

        NotificationModel.save_notification(
            user_id,
            message
        )

        return {

            "status": True,

            "message": "Notification sent successfully"

        }

    @staticmethod
    def get_user_notifications(user_id):

        notifications = NotificationModel.get_notifications(
            user_id
        )

        return notifications

