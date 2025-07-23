
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from django.contrib import auth

# Create your views here.


def home(request):
	result=Doctor.objects.all()
	context={
	"result":result
	}
	return render(request,'patient/home.html',context)





def about(request):
	return render(request,'patient/about.html')


from django.shortcuts import render
from .models import Doctor

def alldoctor(request):
    specialization = request.GET.get('specialization')
    if specialization and specialization != "all":
        result = Doctor.objects.filter(specialization__iexact=specialization)
    else:
        result = Doctor.objects.all()
        
    return render(request, 'patient/alldoctor.html', {'result': result})


def contact(request):
	return render(request,'patient/contact.html')



def register(request):
	return render(request,'patient/register.html')



def register_check(request):
	name = request.POST['name']
	email = request.POST['email']
	password = request.POST['password']


	if User.objects.filter(email=email).exists():
		return redirect('/register')
	if User.objects.filter(username=name).exists():
		return redirect('/register')
	User.objects.create_user(username=name,email=email,password=password)
	return redirect('/login')

def login(request):
	return render(request,'patient/login.html')

def login_check(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)

    if user is None:
        return redirect('/login')
    else:
        auth.login(request, user)
        return redirect('/profile')



def appointment(request,id):
	result = Doctor.objects.get(pk=id)
	context={
	'result':result
	}
	return render(request,'patient/appointment.html',context)
from .models import Doctor, Appointment

from django.shortcuts import render

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def book_appointment(request):
    if request.method == 'POST':
        name = request.POST['pname']
        address = request.POST['address']
        phone = request.POST['phone']
        condition = request.POST['condition']
        time = request.POST['time']
        doctor_id = request.POST.get('id')
        payment_method = request.POST['payment_method']
        user = request.user
        doctor = Doctor.objects.get(id=doctor_id)

        # Store form data in session
        request.session['appointment_data'] = {
            'name': name,
            'address': address,
            'phone': phone,
            'condition': condition,
            'time': time,
            'doctor_id': doctor_id,
        }

        if payment_method == 'online':
            # Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            amount = int(doctor.consultation_fee) * 100  # ₹ to paise
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            
            return render(request, 'patient/payment.html', {
                'payment': payment,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': amount,
                'display_rupees':doctor.consultation_fee,

                'doctor': doctor
            })
        else:
            Appointment.objects.create(
                p_name=name,
                p_address=address,
                p_number=phone,
                p_problem=condition,
                s_time=time,
                user=user,
                doctor=doctor,
                payment_method=payment_method,
            )
            return redirect('profile')


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
import razorpay
from .models import Appointment, Doctor
from django.conf import settings

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.session.get('appointment_data')
        payment_id = request.POST.get('razorpay_payment_id')

        if data:
            doctor = Doctor.objects.get(id=data['doctor_id'])
            amount = int(doctor.consultation_fee) * 100

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            try:
                # ✅ Explicitly capture the payment
                capture_response = client.payment.capture(payment_id, amount)
                print("✅ Payment Captured:", capture_response)

                # ✅ Save appointment
                Appointment.objects.create(
                    p_name=data['name'],
                    p_address=data['address'],
                    p_number=data['phone'],
                    p_problem=data['condition'],
                    s_time=data['time'],
                    user=request.user,
                    doctor=doctor,
                    payment_method='online',
                    razorpay_payment_id=payment_id
                )

                # ✅ Clean up session
                del request.session['appointment_data']

            except Exception as e:
                print("❌ Error capturing payment:", e)
                return HttpResponseBadRequest("Payment capture failed")

        return redirect('profile')
    return HttpResponseBadRequest("Invalid Request")




def contact_check(request):
	name=request.POST['name']
	email=request.POST['email']
	subject=request.POST['subject']
	message=request.POST['message']

	Contact.objects.create(name=name,email=email,subject=subject,message=message)
	return redirect('/contact')




def profile(request):
	user=request.user
	appointment=Appointment.objects.filter(user=user)

	context={
	"user":user,
	"appointment":appointment
	}




	return render(request,'patient/profile.html',context)	




def logout(request):
    auth.logout(request)
    return redirect('home')


def payment(request):
    return render(request, 'patient/payment.html')





def feedback(request,id):
	result=Doctor.objects.get(pk=id)
	context={
	'result':result
	}
	return render(request,'patient/feedback.html',context)


def feedback_check(request):
	doctor_id=request.POST.get('id')
	doctor=Doctor.objects.get(id=doctor_id)





	user=request.user
	star=request.POST['star']
	message=request.POST['message']

	Feedback.objects.create(doctor=doctor,user=user,star=star,message=message)
	return redirect('/profile')



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import razorpay



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment
import razorpay
from django.conf import settings

@csrf_exempt
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id, user=request.user)

    if request.method == 'POST':
        reason = request.POST['reason']
        appointment.status = 'cancelled'
        appointment.cancellation_reason = reason

        if appointment.payment_method == 'online' and not appointment.is_refunded:
            try:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

                if appointment.razorpay_payment_id:
                    print("🔁 Initiating refund for:", appointment.razorpay_payment_id)

                    # ✅ Check if the payment is captured
                    payment_info = client.payment.fetch(appointment.razorpay_payment_id)
                    if payment_info['status'] == 'captured':
                        refund = client.payment.refund(appointment.razorpay_payment_id)
                        appointment.is_refunded = True
                        print("✅ Refund successful:", refund)
                    else:
                        print("❌ Refund failed: Payment not captured. Current status:", payment_info['status'])

                else:
                    print("❌ Razorpay Payment ID missing.")

            except Exception as e:
                print("❌ Refund failed:", str(e))

        appointment.save()
        return redirect('profile')

    context = {'appointment': appointment}
    return render(request, 'patient/cancel_appointment.html', context)
