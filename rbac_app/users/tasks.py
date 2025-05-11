from celery import shared_task
from .models import Record, CustomUser

@shared_task
def delete_records_task(user_id):
    """Delete records for a given user ID after 15 minutes"""
    user = CustomUser.objects.filter(id=user_id).first()
    if user:
        Record.objects.filter(user=user).delete()

# import smtplib
#
# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.ehlo()
# server.starttls()
# server.login("optionalmail3435@gmail.com", "sangram3435")
# print("Login successful")
# server.quit()
