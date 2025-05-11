# # from django.contrib import admin
# # from .models import *
# # # Register your models here.
# #
# # admin.site.register(CustomUser)
# #
# # class MemberAdmin(admin.ModelAdmin):
# #     list_display = ("user", "title", "description",)
# #
# #
# # admin.site.register(Record, MemberAdmin)
#
# from django.contrib import admin
# from django.utils.html import format_html
# from django.core.mail import send_mail
# from django.utils.timezone import now
# from django.db.models import Q
# from django.contrib import messages
# import threading
# import time
#
# from .models import *
#
# class RecordAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'description', 'role', 'user', 'complete_action')
#     list_filter = ('role',)
#     actions = ['mark_as_complete']  # ✅ Define as a list, not a method
#
#     def get_queryset(self, request):
#         """Filter records based on user role"""
#         qs = super().get_queryset(request)
#         if request.user.is_superuser or request.user.role == 'admin':
#             return qs  # Admins can see all records
#         return qs.filter(user=request.user)  # Employees see only their records
#
#     def complete_action(self, obj):
#         """Show a Complete button for admin users"""
#         return format_html(
#             '<a class="button" href="{}">Complete</a>',
#             f"/admin/complete/{obj.id}/"
#         )
#     complete_action.short_description = 'Action'
#
#     def mark_as_complete(self, request, queryset):
#         """Mark selected records as complete"""
#         for record in queryset:
#             send_mail(
#                 "Your Record has been processed",
#                 f"Hello {record.user.username},\n\nYour record titled '{record.title}' has been completed.",
#                 "admin@example.com",
#                 [record.user.email],
#                 fail_silently=False,
#             )
#
#             # Schedule deletion after 15 minutes
#             def delete_record():
#                 time.sleep(900)
#                 record.delete()
#                 messages.success(request, f"Record '{record.title}' deleted after 15 minutes.")
#
#             threading.Thread(target=delete_record).start()
#
#         messages.success(request, "Records marked as completed and scheduled for deletion.")
#
#     mark_as_complete.short_description = "Mark selected records as complete"
#
# admin.site.register(Record, RecordAdmin)
#
# admin.site.register(CustomUser)



# -----------------------------------
#
# from django.contrib import admin
# from django.utils.html import format_html
# from django.core.mail import send_mail
# from django.utils.timezone import now
# from django.db.models import Count
# from django.urls import reverse
# import threading
# import time
#
# from .models import Record, CustomUser
#
#
# class EmployeeRecordAdmin(admin.ModelAdmin):
#     list_display = ('sn', 'employee_name', 'record_count', 'complete_action')
#     list_filter = ('user',)
#
#     def get_queryset(self, request):
#         """Return queryset for records"""
#         qs = super().get_queryset(request)
#
#         # Employees see only their own records, Admins see all
#         if request.user.role == 'employee':
#             return qs.filter(user=request.user)
#         return qs
#
#     def get_employee_data(self):
#         """Return aggregated record count per employee"""
#         return Record.objects.values('user__id', 'user__username').annotate(record_count=Count('id'))
#
#     def sn(self, obj):
#         """Serial number"""
#         employees = list(self.get_employee_data())
#         for index, emp in enumerate(employees):
#             if emp['user__id'] == obj.user.id:
#                 return index + 1
#         return "-"
#     sn.short_description = "SN"
#
#     def employee_name(self, obj):
#         """Display employee name"""
#         return obj.user.username
#     employee_name.short_description = "Name of Employee"
#
#     def record_count(self, obj):
#         """Display number of records per employee"""
#         return Record.objects.filter(user=obj.user).count()
#     record_count.short_description = "No. of Records"
#
#     def complete_action(self, obj):
#         """Show a Complete button for admin users"""
#         if obj.user.role == 'employee' and self.record_count(obj) > 0:
#             complete_url = reverse('complete_record', args=[obj.user.id])  # ✅ Corrected URL
#             return format_html('<a class="button" href="{}">Complete</a>', complete_url)
#         return "-"
#     complete_action.short_description = 'Action'
#
#     def mark_as_complete(self, request, queryset):
#         """Mark selected employees' records as complete"""
#         if not request.user.is_superuser:
#             self.message_user(request, "Permission denied.", level='error')
#             return
#
#         for record in queryset:
#             user_email = record.user.email
#
#             if user_email:
#                 send_mail(
#                     "Your Records have been processed",
#                     f"Hello {record.user.username},\n\nYour records have been completed.",
#                     "admin@example.com",
#                     [user_email],
#                     fail_silently=False,
#                 )
#
#                 # Schedule deletion after 15 minutes
#                 def delete_records():
#                     time.sleep(900)  # 15 minutes delay
#                     Record.objects.filter(user=record.user).delete()
#
#                 threading.Thread(target=delete_records).start()
#
#         self.message_user(request, "Records marked as completed and scheduled for deletion.")
#
#     mark_as_complete.short_description = "Mark selected employees' records as complete"
#     actions = ['mark_as_complete']
#
#
# admin.site.register(Record, EmployeeRecordAdmin)



# ------------------------------------------------------------------------


# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import redirect, get_object_or_404
# from django.utils.html import format_html
# from django.contrib import messages
# from django.utils.timezone import now
# import threading
# import time
#
# from django.core.mail import send_mail
# from .models import CustomUser, Record
#
#
# class RecordAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "description", "user")
#
#     def get_queryset(self, request):
#         """Employees see only their own records, admins see all records."""
#         qs = super().get_queryset(request)
#         if request.user.role == 'employee':
#             return qs.filter(user=request.user)
#         return qs  # Admins see all records
#
# admin.site.register(Record, RecordAdmin)
# from django.contrib import admin, messages
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import path
# from django.utils.html import format_html
# from django.core.mail import send_mail
# import time
# import threading
#
# from .models import CustomUser, Record  # Ensure correct import
#
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("id", "username", "name_of_employee", "role", "record_count", "complete_action")
#
#     def name_of_employee(self, obj):
#         """Return the full name of the employee"""
#         return CustomUser.objects.all().count()
#         # return obj.username  # Change `name` to the correct field if different
#
#     name_of_employee.short_description = "Name Of Employee"
#
#     def record_count(self, obj):
#         """Count the number of records associated with the user."""
#         return Record.objects.all().count()
#
#     record_count.short_description = "No of Records"
#
#     def complete_action(self, obj):
#         """Show a 'Complete' button for admin users if records exist"""
#         if obj.role == 'employee' and self.record_count(obj) > 0:
#             complete_url = f"complete/{obj.id}/"  # Adjusted URL
#             return format_html('<a class="button" href="{}">Complete</a>', complete_url)
#         return "-"
#
#     complete_action.short_description = "Action"
#
#     def get_urls(self):
#         """Add custom URLs inside the Django Admin"""
#         urls = super().get_urls()
#         custom_urls = [
#             path('complete/<int:user_id>/', self.admin_site.admin_view(self.complete_record), name="complete_record"),
#         ]
#         return custom_urls + urls
#
#     def complete_record(self, request, user_id):
#         """Admin action: Complete the user's records, send email, and schedule deletion"""
#         user = get_object_or_404(CustomUser, id=user_id)
#
#         # Send email notification
#         if user.email:
#             send_mail(
#                 "Your Records have been processed",
#                 f"Hello {user.username},\n\nYour records have been completed.",
#                 "admin@example.com",
#                 [user.email],
#                 fail_silently=False,
#             )
#
#         # Schedule deletion after 15 minutes
#         def delete_records():
#             time.sleep(900)  # 15 minutes delay
#             Record.objects.filter(user=user).delete()
#
#         threading.Thread(target=delete_records).start()
#
#         messages.success(request, f"Records for {user.username} marked as complete and scheduled for deletion.")
#         return redirect("..")
#
# admin.site.register(CustomUser, CustomUserAdmin)



# ------------------------------------------------------


#
#
# from django.contrib import admin, messages
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import path
# from django.utils.html import format_html
# from django.core.mail import send_mail
# from django.contrib.auth.models import Group
# from .utils import send_email_to_client
#
# from .models import CustomUser, Record
# from .tasks import delete_records_task  # Import Celery task
#
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("id", "username", "name_of_employee", "role", "record_count", "complete_action")
#
#     def name_of_employee(self, obj):
#         """Return the employee's username"""
#         return obj.username
#
#     name_of_employee.short_description = "Name Of Employee"
#
#     def record_count(self, obj):
#         """Count the number of records associated with the user."""
#         return Record.objects.filter(user=obj).count()  # Corrected to filter per user
#
#     record_count.short_description = "No of Records"
#
#     # def complete_action(self, obj):
#     #     """Show 'Complete' button for admins only if the user has records"""
#     #     if obj.role == "admin":  # Only show to admins
#     #         if self.record_count(obj) > 0:  # Ensure records exist
#     #             complete_url = f"complete/{obj.id}/"
#     #             return format_html('<a class="button" href="{}">Complete</a>', complete_url)
#     #     return "-"
#
#     def complete_action(self, obj):
#         """Show 'Complete' button for admins only if the user has records.
#            When clicked, it completes the action and sends an email.
#         """
#         if obj.role == "admin":  # Only show to admins
#             if self.record_count(obj) > 0:  # Ensure records exist
#                 complete_url = f"complete/{obj.id}/"
#
#                 # Call the email function
#                 send_email_to_client()
#
#                 return format_html('<a class="button" href="{}">Complete</a>', complete_url)
#
#         return "-"
#
#     complete_action.short_description = "Action"
#
#     def get_urls(self):
#         """Add custom URLs inside the Django Admin"""
#         urls = super().get_urls()
#         custom_urls = [
#             path('complete/<int:user_id>/', self.admin_site.admin_view(self.complete_record), name="complete_record"),
#         ]
#         return custom_urls + urls
#
#     def complete_record(self, request, user_id):
#         """Admin action: Complete user's records, send email, and schedule deletion"""
#         user = get_object_or_404(CustomUser, id=user_id)
#         records = Record.objects.filter(user=user)
#
#         if not records.exists():
#             messages.warning(request, f"No records found for {user.username}.")
#             return redirect("..")
#
#         # Send email notification
#         if user.email:
#             send_mail(
#                 "Your Records have been processed",
#                 f"Hello {user.username},\n\nYour records have been completed.",
#                 "admin@example.com",
#                 [user.email],
#                 fail_silently=False,
#             )
#
#         # Schedule deletion using Celery
#         delete_records_task.apply_async(args=[user.id], countdown=900)  # 15 min delay
#
#         messages.success(request, f"Records for {user.username} marked as complete and scheduled for deletion.")
#         return redirect("..")
#
# admin.site.register(CustomUser, CustomUserAdmin)



# 25 march ---------------------------------------------------------------------------------


from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import CustomUser, Record
from .tasks import delete_records_task  # Import Celery task
from .utils import send_email_to_client

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "name_of_employee", "role", "record_count", "complete_action")

    def name_of_employee(self, obj):
        """Return the employee's username"""
        return obj.username

    name_of_employee.short_description = "Name Of Employee"

    def record_count(self, obj):
        """Count the number of records associated with the user."""
        return Record.objects.filter(user=obj).count()  # Filters records per user

    record_count.short_description = "No of Records"

    def complete_action(self, obj):
        """
        Show 'Complete' button for admins only.
        - If the employee has records, show the button.
        - Clicking the button triggers email and schedules deletion.
        """
        if obj.role != "admin" and self.record_count(obj) > 0:  # Only for employees with records
            complete_url = reverse("admin:complete_record", args=[obj.id])
            return format_html('<a class="button" href="{}">Complete</a>', complete_url)
        return "-"

    complete_action.short_description = "Action"

    def get_urls(self):
        """Add custom URLs inside the Django Admin"""
        urls = super().get_urls()
        custom_urls = [
            path('complete/<int:user_id>/', self.admin_site.admin_view(self.complete_record), name="complete_record"),
        ]
        return custom_urls + urls

    def complete_record(self, request, user_id):
        """Admin action: Complete user's records, send email, and schedule deletion"""
        user = get_object_or_404(CustomUser, id=user_id)
        records = Record.objects.filter(user=user)

        if not records.exists():
            messages.warning(request, f"No records found for {user.username}.")
            return redirect("..")

        # Send email notification
        send_email_to_client(user.email, user.username, records)

        # Schedule deletion using Celery (15-minute delay)
        delete_records_task.apply_async(args=[user.id], countdown=900)

        messages.success(request, f"Records for {user.username} marked as complete and scheduled for deletion.")
        return redirect("..")

admin.site.register(CustomUser, CustomUserAdmin)
