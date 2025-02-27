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
            subject = "Enrollment Confirmation - TechAkili Technologies"
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


