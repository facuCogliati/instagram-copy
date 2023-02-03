from .models import Notifications
def createNotifications(sender, user, type, post):
    if not post:
        Notifications.objects.create(
            type = 1,
            sender = sender,
            user = user,
        )
    return