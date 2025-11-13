from . import ma
from .models import Notification

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True

notification_schema = NotificationSchema()
notifications_schema = NotificationSchema(many=True)