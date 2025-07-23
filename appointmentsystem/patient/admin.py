from django.contrib import admin
from .models import *

# Customize admin for Doctor
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialization', 'email', 'phone']  # Replace with actual fields
    search_fields = ['name', 'specialization', 'email', 'phone']
    list_filter = ['specialization']

# Customize admin for Contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message']  
    search_fields = ['name', 'email', 'subject', 'message']
    list_filter = ['name']


class AppointmentAdmin(admin.ModelAdmin):
    a=['','p_address','p_number','p_problem','s_time','user','doctor']
    b=['','p_address','p_number','p_problem','s_time','user','doctor']
    c=['p_name','p_address','p_number','p_problem','s_time','user','doctor']



class FeedbackAdmin(admin.ModelAdmin):
    a=['star','message','user','doctor']
    b=['star','message','user','doctor']
    c=['star','message','user','doctor']


admin.site.register(Feedback,FeedbackAdmin)

admin.site.register(Appointment, AppointmentAdmin)

# Register models with custom admin
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Contact, ContactAdmin)
