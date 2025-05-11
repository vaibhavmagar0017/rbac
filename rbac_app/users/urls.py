from django.contrib import admin
from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', login_page, name='login_page'),
    path('register_page/', register_page, name='register_page'),
    path('send_mail_page/', send_mail_page),

    path('dashboard/', dashboard, name='dashboard'),
    path('user_logout/', user_logout, name='user_logout'),
    path('view_records/', view_records, name='view_records'),
    path('upload_records/', upload_records, name='upload_records'),
    path('export_records/', export_records, name='export_records'),
    path('edit_record/<int:record_id>/', edit_record, name='edit_record'),  # Ensure this is correct
    path('delete_record/<int:record_id>/', delete_record, name='delete_record'),  # Add this if missing
    path('admin/complete/<int:record_id>/', complete_record, name='complete_record'),
    path('admin/complete/<int:user_id>/', complete_record, name='complete_record'),
    path('send_email/', send_email, name='send_email'),
    path('email_attachment/', email_attachment, name='email_attachment'),

]
















