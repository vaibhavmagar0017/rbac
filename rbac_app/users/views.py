import time
import csv
import threading
import pandas as pd

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .models import CustomUser, Record
from .utils import send_email_normal, send_email_with_attachment


def complete_record(request, user_id):
    """Mark the user's records as completed, send email, and schedule deletion."""
    user = get_object_or_404(CustomUser, id=user_id)

    # Send email notification to the employee
    if user.email:
        send_mail(
            "Your Records have been processed",
            f"Hello {user.username},\n\nYour records have been completed.",
            "admin@example.com",
            [user.email],
            fail_silently=False,
        )

    # Schedule deletion after 15 minutes
    def delete_records():
        time.sleep(900)  # 15 minutes delay
        Record.objects.filter(user=user).delete()

    threading.Thread(target=delete_records).start()

    messages.success(request, f"Records for {user.username} marked as complete and scheduled for deletion.")
    return redirect('/admin/users/record/')

# -------------------------------------------------

def dashboard(request):
    return render(request, 'dashboard.html')

def edit_record(request, record_id):
    """ Placeholder edit function (modify as needed) """
    return HttpResponse(f"Edit record {record_id}")  # Replace with actual logic


@login_required
def delete_record(request, record_id):
    """ Delete a record by ID """
    record = get_object_or_404(Record, id=record_id)

    # Ensure the user can delete the record (optional)
    if request.user.role == record.role:
        record.delete()

    return redirect('view_records')  # Redirect after deletion

def view_records(request):
    """ View records based on the user's role """
    if request.user.role in ['admin', 'employee']:
        records = Record.objects.filter(role=request.user.role)  # Show records for the current user's role
        return render(request, 'view.html', {'records': records})
    return redirect('dashboard')  # Redirect unauthorized users


# export records
@login_required
def upload_records(request):
    """ Upload records from a CSV file """
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():
            Record.objects.create(
                user=request.user,
                title=row.get('title', 'test'),
                description=row.get('description', ''),
                role=request.user.role  # Assign the logged-in user's role
            )

        return redirect('view_records')  # Redirect to view_records after upload

    return render(request, 'upload.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username = username,
            password = password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("Invalid username password", status=400)

    return render(request, 'login.html')


@login_required
def register_page(request):  # register_page function is correct, but I'm not clear UI code
    """
    Handle user registration.

    If the request method is POST, process the registration form.
    If the username already exists, display an error message.
    Otherwise, create a new user, save the password securely, and redirect to login.
    """
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect("register")  # Use named URL patterns instead of hardcoded paths

        # Create and save the user
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect("login")  # Use named URL patterns

    return render(request, "register.html")


@login_required
def export_records(request):
    """ Export records to CSV if user is admin """
    if request.user.role == 'admin':
        records = Record.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content_Disposition'] = 'attachment; filename="records.csv"'

        writer = csv.writer(response)
        writer.writerows(['User', 'Title'])

        for record in records:
            writer.writerows([record.user.username, record.title])

        return response

    else:
        return HttpResponse("Do not have permission")


def user_logout(request):
    """ Log out the user and redirect to home page """
    logout(request)
    return redirect('/')


# Send Email
def send_email(request):
    send_email_normal() # call utils function
    return redirect('dashboard')


# Send Email with attachment
def email_attachment(request):
    """View to send an email with an attachment and return an HTTP response"""
    file_path = f"{settings.BASE_DIR}/xyz.xlsx"  # Replace with the actual file path
    recipient_list = ["dev@smartscripts.in"]  # Replace with actual recipients

    try:
        send_email_with_attachment(
            subject="Test Email with Attachment",
            message="Hello, please find the attached file.",
            recipient_list=recipient_list,
            file_path=file_path
        )
        return HttpResponse("Email sent successfully with an attachment.")  # ✅ Return response

    except Exception as e:
        return HttpResponse(f"Error sending email: {e}", status=500)  # ✅ Return error response


# send mail on page side
def send_mail_page(request):
    """
    View to send an email based on user input from a form.
    :param request:
    :return:
    """
    context = {}

    if request.method == 'POST':
        address = request.POST.get('address')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if address and subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
                print('-------------------------', send_mail)
                context['result'] = 'Email sent successfully'
            except Exception as e:
                context['result'] = f'Error sending email: {e}'
        else:
            context['result'] = 'All fields are required'

    return render(request, "index.html", context)
