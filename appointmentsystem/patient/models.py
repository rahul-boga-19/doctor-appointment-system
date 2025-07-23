from django.db import models

# Create your models here.



class Doctor(models.Model):
	d_image=models.ImageField()
	name = models.CharField(max_length=255)
	qualification = models.CharField(max_length=255)
	experience = models.CharField(max_length=255)
	specialization=models.CharField(max_length=255)
	consultation_fee=models.CharField(max_length=255)
	phone=models.BigIntegerField()
	email=models.CharField(max_length=255)
	description=models.CharField(max_length=255)




from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    p_name = models.CharField(max_length=100)
    p_address = models.TextField()
    p_number = models.CharField(max_length=15)
    p_problem = models.TextField()
    s_time = models.CharField(max_length=100)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('cancelled', 'Cancelled')], default='scheduled')
    cancellation_reason = models.TextField(blank=True, null=True)
    is_refunded = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.p_name} - {self.doctor.name}"



class Contact(models.Model):
	name=models.CharField(max_length=50)
	email=models.CharField(max_length=50)
	subject=models.CharField(max_length=100)
	message=models.TextField()



class Feedback(models.Model):
	star=models.CharField(max_length=255)
	message=models.TextField()
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)