import os
from email.message import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings


# send_email_normal (This function call into views.py)
def send_email_normal():
    subject = "This email from django server"
    message = "This is test"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["dev@smartscripts.in"]
    send_mail(subject, message, from_email, recipient_list)

# Send email with attachment (This function call in views.py)
def send_email_with_attachment(subject, message, recipient_list, file_path):
    """Send an email with an attachment"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list
        )
        mail.attach_file(file_path)
        mail.send(fail_silently=False)

        print(f"Email sent successfully to {recipient_list}")

    except Exception as e:
        print(f"Error sending email: {e}")


# util.py <--- This function call into admin.py
def send_email_to_client(email, username, records):
    """Send email to the specified user with their records."""
    subject = "Your Records have been processed"
    message = f"Hello {username},\n\nYour records have been completed.\n\nTotal Records: {len(records)}"
    from_email = "dev@smartscripts.in"

    send_mail(subject, message, from_email, [email], fail_silently=False)
