from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .forms import LoginForm  
from django.contrib.auth import get_user_model
from .forms import EnrollmentForm
from django.core.mail import send_mail
from django.conf import settings
from publicpages.models import Enrollment  
from .forms import PartnershipForm
from django.core.mail import send_mail
from .models import Partnership





def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def courses(request):
    return render(request, 'courses.html')

def partners(request):
    return render(request, 'partners.html')

def careers(request):
    return render(request, 'careers.html')

def contact(request):
    return render(request, 'contact.html')


def submit_partnership(request):
    return render(request, 'submit_partnership.html')

def team(request):
    return render(request, 'ourteam.html')

def mission(request):
    return render(request, 'mission.html')

def training_and_workshops(request):
    return render(request, 'training_and_workshops.html')

def consulting(request):
    return render(request, 'consulting.html')

def attarch(request):
    return render(request, 'attarch.html')

def intern(request):
    return render(request, 'intern.html')

def register_workshop(request):
    return render(request, 'register_workshop.html')

def workshop_detail(request):
    return render(request, 'workshop_detail.html')

# Authentication Views
User = get_user_model()

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm  # Ensure your form is correctly imported

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Ensure password is hashed
            user.save()

            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")  # Redirect to login page
        else:
            messages.error(request, "Please correct the errors below.")  # Show errors if form is invalid
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})  # Return the form page with errors (if any)

User = get_user_model()

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        remember_me = request.POST.get("remember_me") == "on"

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            request.session.set_expiry(1209600 if remember_me else 0)
            return redirect("home")
        else:
            form.add_error(None, "Invalid email or password")

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def forgot_password_view(request):
    return render(request, 'forgot_password.html')


def enroll(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment successful!")
            return redirect("courses")  # Redirect to courses page after enrollment
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = EnrollmentForm()
    
    return render(request, "enroll.html", {"form": form})


def enroll(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()

            # Send Confirmation Email
            subject = "Enrollment Confirmation "
            message = f"Hello {enrollment.name},\n\nThank you for enrolling in {enrollment.course}!\nWe will reach out soon with further details.\n\nBest,\nTechAkili Technologies"
            recipient = [enrollment.email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)

            messages.success(request, "Enrollment successful! Check your email for confirmation.")
            return redirect("courses")  
        else:
            messages.error(request, "There was an error with your submission.")
    
    else:
        form = EnrollmentForm()
    
    return render(request, "enroll.html", {"form": form})



def submit_partnership(request):
    if request.method == 'POST':
        form = PartnershipForm(request.POST)
        if form.is_valid():
            partnership = form.save()

            # Send email notification
            subject = f"New Partnership Application from {partnership.organization_name}"
            message = f"""
            Organization Name: {partnership.organization_name}
            Contact Person: {partnership.contact_person}
            Email: {partnership.email}
            Phone: {partnership.phone}
            Partnership Type: {partnership.get_partnership_type_display()}
            Message: {partnership.message}
            """
            send_mail(subject, message, 'your_email@gmail.com', ['ramspheldonyango@gmail.com'])


            messages.success(request, "Your partnership request has been submitted successfully!")
            return redirect('partners')
        else:
            messages.error(request, "There was an error submitting your request.")
    
    else:
        form = PartnershipForm()
    
    return render(request, 'partners.html', {'form': form})


from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings

def contact_form_submission(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Send an email
        send_mail(
            subject=f"New Contact Form Submission from {fullname}",
            message=f"Name: {fullname}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['ramspheldonyango@gmail.com'],  # Change to your email
            fail_silently=False,
        )

    
        return JsonResponse({'success': True, 'message': 'Your message has been sent!'})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


# views.py

from django.shortcuts import render, redirect
from paypalrestsdk import Payment
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def paypal_donate(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/donate/success/",
                "cancel_url": "http://127.0.0.1:8000/donate/cancel/"
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Donation to support our cause."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)  # Redirect user to PayPal

        return render(request, "donate3.html", {"error": "Error processing payment"})

    return render(request, "donate3.html")


def donate_success(request):
    return render(request, "success.html")


def donate_cancel(request):
    return render(request, "cancel.html")

from django.shortcuts import render
from django.http import JsonResponse
from .mpesa_utils import stk_push

def initiate_mpesa_payment(request):
    if request.method == "POST":
        phone = request.POST.get("phone")  # User's phone number
        amount = request.POST.get("amount")  # Donation amount

        response = stk_push(phone, amount)
        return JsonResponse(response)  # Return M-Pesa STK Push response

    return render(request, "donate.html")

from django.shortcuts import render

def mpesa_donate(request):
    return render(request, 'donate_paypal.html')

def donate(request):
    return render(request, 'donate.html')

import requests
import base64
import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger(__name__)

# MPesa credentials
CONSUMER_KEY = "g8OoexGzOynPsv37sCsaVDaBLa23u8ik9DYVnUFmJyoiz4In"
CONSUMER_SECRET = "mJT2rApRrJHkECmtB9UMCxXTXlCVwQyA91UU9K0R1CW29mB8iGKcGNx1NIjC2LNp"
PASSKEY = "YOUR_PASSKEY"  # Update with actual passkey
BUSINESS_SHORTCODE = "YOUR_SHORTCODE"  # Update with actual shortcode
CALLBACK_URL = "https://yourdomain.com/mpesa/callback/"

# Get MPesa Access Token
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        logger.error(f"MPesa Token Error: {e}")
        return None

# Initiate STK Push
def stk_push(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        # Ensure phone is formatted correctly
        if phone.startswith("0"):
            phone = "254" + phone[1:]

        access_token = get_access_token()
        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=500)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

        payload = {
            "BusinessShortCode": BUSINESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": BUSINESS_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Test Payment",
            "TransactionDesc": "Payment for service"
        }

        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        try:
            response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
            response.raise_for_status()
            return JsonResponse(response.json())
        except requests.exceptions.RequestException as e:
            logger.error(f"MPesa STK Push Error: {e}")
            return JsonResponse({"error": "Failed to process request"}, status=500)

    return render(request, "mpesa_payment.html")

# Handle MPesa Callback
def mpesa_callback(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        logger.info(f"MPesa Callback Response: {json.dumps(data, indent=2)}")
        return JsonResponse({"status": "Received"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# Render MPesa Payment Page
def mpesa_payment(request):
    return render(request, "mpesa_payment.html")
