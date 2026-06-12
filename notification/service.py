from .repository import NotificationRepo

class NotificationService:

    repo = NotificationRepo()

    def get_notifications(self , recipient , is_read):
        return self.repo.get_notifications(recipient = recipient , is_read = is_read)
    
    def mark_as_read(self , recipient):
        return self.repo.mark_as_read(recipient)
    
    def create_notification(self):pass