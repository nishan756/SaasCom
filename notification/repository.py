from .models import Notification


class NotificationRepo:

    def get_notifications(self , recipient , is_read):
        notifications = Notification.objects.filter(recipient = recipient).select_related("recipient" , "actor")

        if is_read:
            notifications = notifications.filter(is_read = is_read)

        return notifications
    
    def mark_as_read(self , recipient):
        return Notification.objects.filter(is_read = False , recipient = recipient).update(is_read = True)
    
    def create_notification(self):pass
    