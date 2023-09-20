from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Ashaworker
from .models import Appointment
from .models import PatientProfile
from .models import Image 
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect



from django.contrib.auth import get_user_model
# Create your views here.



User=get_user_model()

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def treatment(request):
    return render(request,'treatment.html')

def testimonial(request):
    return render(request,'testimonial.html')

def contact(request):
    return render(request,'contact.html')

def patients(request):
    return render(request,'admin_temp/patients.html')

def schedule(request):
    return render(request,'admin_temp/schedule.html')

def index2(request):
    return render(request,'admin_temp/index-2.html')

def addpatient(request):
    return render(request,'admin_temp/add-patient.html')




def edit_patient_profile(request):
    
    # user = request.user
    # profile = PatientProfile.objects.get(user=user)
    user = request.user
    profile = get_object_or_404(PatientProfile, user=user)
    
    if request.method == "POST":
        print ('POST')
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        # Process the form data and save/update the profile

        profile.first_name = request.POST.get('first_name')
        print("first name :",profile.first_name)
        
        profile.last_name = request.POST.get('last_name')
        print("last name :",profile.last_name)

    
        profile.email = request.POST.get('email')
        print("email name :",profile.email)

        profile.gender = request.POST.get('gender')
        print("gender :",profile.gender)

        profile.house_name = request.POST.get('house_name')
        print("house name :",profile.house_name)

        profile.house_no = request.POST.get('house_no')
        print("house no :",profile.house_no)

        profile.address = request.POST.get('address')
        print("adsress :",profile.address)

        profile.ward = request.POST.get('ward')
        print("ward :",profile.ward)

        profile.pin_code = request.POST.get('pin_code')
        print("pin code :",profile.pin_code)

        profile.phone_number = request.POST.get('phone_number')
        print("phone :",profile.phone_number)

        profile.current_diagnosis = request.POST.get('current_diagnosis')
        print("curret dignosis :",profile.current_diagnosis)

        profile.past_med_condition = request.POST.get('past_med_condition')
        print("past medicine :",profile.past_med_condition)

        profile.surgical_history = request.POST.get('surgical_history')
        print("surgical histroy :",profile.surgical_history)

        profile.allergies = request.POST.get('allergies')
        print("allergies :",profile.allergies)

        profile.height = request.POST.get('height')
        print("height :",profile.height)

        profile.weight = request.POST.get('weight')
        print("weight :",profile.weight)

        profile.bmi = request.POST.get('bmi')
        print("bmi :",profile.bmi)

        profile.medication_names = request.POST.get('medication_names')
        print("medicine names :",profile.medication_names)

        profile.dosage = request.POST.get('dosage')
        print("dosage :",profile.dosage)

        profile.frequency = request.POST.get('frequency')
        print("frequency :",profile.frequency)
        new_profile_pic = request.FILES.get('profile_pic')

        if new_profile_pic:
            # Save the profile photo to a specific directory
            fs = FileSystemStorage()
            filename = fs.save(f"profile_pics/{new_profile_pic.name}", new_profile_pic)
            profile.profile_pic = filename       
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('print_patient_profile')  # Redirect to the profile page
    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'edit_patient_profile.html',context) 


def print_patient_profile(request):
    profile = PatientProfile.objects.filter(user=request.user).first() 
    return render(request, 'print_patient_profile.html', {'profile': [profile]})

@login_required(login_url='login_page')
def ad_appointment(request):
    appo = Appointment.objects.all()
    return render(request, 'admin_temp/appointments.html', {'appo': appo})

# def approved_appointments(request):
#     return render(request, 'asha_temp/asha_approved_appo.html')


def asha_approved_appointments(request):
    approved_appointments = Appointment.objects.filter(is_approved=True)
    print(approved_appointments)
    return render(request, 'asha_temp/asha_approved_appo.html', {'approved_appointments': approved_appointments})



from django.shortcuts import get_object_or_404, redirect

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.is_approved = True
    appointment.save()
    
    # Redirect back to the list of approved appointments
    return redirect("asha_approved_appo")


def patient_users(request):
    # patients = CustomUser.objects.filter(role=CustomUser.PATIENTS)
    patients = PatientProfile.objects.filter()
    return render(request, 'asha_temp/patient_users.html', {'patients': patients})










@login_required(login_url='login_page')
def appointment_form(request,appointment_id=None):
    patientprofile = request.user.patientprofile
    time_slots = []  # Initialize an empty list for time slots

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        ward_asha = request.POST.get('ward')
        phone_number = request.POST.get('phone_number')
        # id_proof = request.FILES.get('id_proof')
        medical_conditions = request.POST.get('medical_conditions')
        urgency = request.POST.get('urgency')
        medication_names= request.POST.get('medication_names')
        symptoms = request.POST.get('symptoms')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')

        # Create an appointment object and save it to the database
        appointment = Appointment(
            first_name=first_name,
            last_name=last_name,
            email=email,
            # date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            ward_asha=ward_asha,
            phone_number=phone_number,
            # id_proof=id_proof,
            medical_conditions=medical_conditions,
            urgency=urgency,
            medication_names=medication_names,
            symptoms=symptoms,
            preferred_date=preferred_date,
            preferred_time=preferred_time
        )
        appointment.save()

        return render(request,'appointment.html')
        # return render(request, 'appointment.html')

    else:
        # Generate time slots with 30-minute intervals for AM and PM
        start_time = datetime.strptime("06:00 AM", "%I:%M %p")
        end_time = datetime.strptime("09:00 PM", "%I:%M %p")
        interval = timedelta(minutes=30)

        while start_time <= end_time:
            time_slots.append(start_time.strftime("%I:%M %p"))
            start_time += interval

    return render(request, 'appointment.html', {'time_slots': time_slots,'patientprofile': patientprofile,'appointment_id': appointment_id})

from django.contrib.auth.decorators import login_required
@login_required(login_url='login_page')
def add_asha(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        doj = request.POST.get('doj')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        ward = request.POST.get('ward')
        pin = request.POST.get('pin')
        phone = request.POST.get('phone')
        # user.role=ASHAWORKER
        role=CustomUser.ASHAWORKER
        # Handle profile photo upload
        profile_photo = request.FILES.get('profile_photo')

        # Create an instance of Ashaworker
        obj = Ashaworker()
        user=CustomUser()
        obj.Name = name
        obj.email = email
        obj.set_password(password)
        obj.date_of_birth = dob
        obj.date_of_join = doj
        obj.gender = gender
        obj.address = address
        obj.taluk = taluk
        obj.Panchayat = panchayat
        obj.ward = ward
        obj.postal = pin
        obj.phone = phone
        
        user.email=email
        user.set_password(password)
        user.role=role
        if profile_photo:
            # Save the profile photo to a specific directory
            fs = FileSystemStorage()
            filename = fs.save(f"profile_photos/{profile_photo.name}", profile_photo)
            obj.profile_photo = filename  # Associate profile photo if uploaded

        obj.save()
        user.save()
        messages.success(request, 'Asha Worker created successfully!')

        return redirect('ad_ashaworker')

    return render(request, 'admin_temp/add_asha.html')


@login_required(login_url='login')
def ad_ashaworker(request):
    ashaworkers = Ashaworker.objects.all()
    return render(request, 'admin_temp/ad_ashaworker.html', {'ashaworkers': ashaworkers})
    

@login_required(login_url='login_page')
def edit_asha(request, asha_id):
    ashaworker = get_object_or_404(Ashaworker, id=asha_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        dob = request.POST.get('dob')
        doj = request.POST.get('doj')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        ward = request.POST.get('ward')
        pin = request.POST.get('pin')
        phone = request.POST.get('phone')

        ashaworker.Name = name
        ashaworker.email = email
        ashaworker.set_password(password)
        ashaworker.date_of_birth = dob
        ashaworker.date_of_join = doj
        ashaworker.gender = gender
        ashaworker.address = address
        ashaworker.taluk = taluk
        ashaworker.Panchayat = panchayat
        ashaworker.ward = ward
        ashaworker.postal = pin
        ashaworker.phone = phone
        ashaworker.save()
        return redirect('ad_ashaworker')
    return render(request, 'admin_temp/edit_asha.html', {'ashaworker': ashaworker})

from django.shortcuts import render
from .models import Ashaworker

# def search_ashaworker(request):
#     # Get the search query from the GET request
#     search_query = request.GET.get('ashaname', '')

#     # Filter Ashaworkers whose name contains the search query
#     ashaworkers = Ashaworker.objects.filter(Name__icontains=search_query, is_active=True)

#     context = {
#         'ashaworkers': ashaworkers,
#         'search_query': search_query,
#     }

#     return render(request, 'admin_temp/ad_ashaworker.html', context)
def search_ashaworker(request):
    # Get the search query from the GET request
    search_query = request.GET.get('ashaname', '')

    # Filter Ashaworkers whose name contains the search query
    ashaworkers = Ashaworker.objects.filter(Name__icontains=search_query, is_active=True)

    context = {
        'ashaworkers': ashaworkers,
        'search_query': search_query,
    }

    return render(request, 'admin_temp/ad_ashaworker.html', context)











@login_required(login_url='login_page')
def delete_asha(request, asha_id):
    ashaworker = get_object_or_404(Ashaworker, id=asha_id)

    if request.method == 'POST':
        # Set the is_active attribute to False instead of deleting
        ashaworker.is_active = False
        ashaworker.save()

        # Add a success message to the session
        request.session['deleted_asha_success'] = True

        # Redirect to the 'ad_ashaworker' page (or adjust the URL as needed)
        return redirect('ad_ashaworker')

    return render(request, 'admin_temp/delete_asha.html', {'ashaworker': ashaworker})



       
# def admin_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('admin_dashboard')  # Redirect to admin dashboard
#         else:
#             # Invalid credentials, handle error or show message
#             pass
    
#     return render(request, 'admin_temp/adlogin.html')




@login_required(login_url='login_page')
def admin_dashboard(request):

    return render(request, 'admin_temp/adindex.html')






@login_required(login_url='login_page')
def asha_index(request):

    return render(request, 'asha_temp/asha_index.html')

def asha_profile(request):
     
    return render(request, 'asha_temp/asha_profile.html')

# def edit_asha_profile(request):

#     return render(request, 'asha_temp/edit_asha_profile.html')


def edit_asha_profile(request):
    ashaworker = get_object_or_404(Ashaworker)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        dob = request.POST.get('dob')
        doj = request.POST.get('doj')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        ward = request.POST.get('ward')
        pin = request.POST.get('pin')
        phone = request.POST.get('phone')

        ashaworker.Name = name
        ashaworker.email = email
        ashaworker.set_password(password)
        ashaworker.date_of_birth = dob
        ashaworker.date_of_join = doj
        ashaworker.gender = gender
        ashaworker.address = address
        ashaworker.taluk = taluk
        ashaworker.Panchayat = panchayat
        ashaworker.ward = ward
        ashaworker.postal = pin
        ashaworker.phone = phone
        ashaworker.save()
        return redirect('asha_profile')
    return render(request, 'asha_temp/edit_asha_profile.html', {'ashaworker': ashaworker})



def login_page(request):
    # if request.user.is_authenticated:
    #     # User is authenticated, redirect to another page
    #     return render(request, 'appointment.html')


    if request.method == "POST":
        # username=request.POST['email']
        email=request.POST['email']
        password=request.POST['password']
        print(email)
        print(password)
        user = authenticate(email=email,password=password)
        print(user)
        if user is not None:
            
            if user.role == CustomUser.ASHAWORKER:
               login(request, user) 
               return redirect('asha_index')
            elif user.role == CustomUser.PATIENTS:
                login(request, user)
                return redirect('/')
            elif user.role == CustomUser.HCA:
                login(request, user)
                return redirect('/')
            elif user.role == CustomUser.ADMIN:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.info(request, "Invalid Role for Login")
        else:
            messages.info(request, "Invalid Login")
        return redirect('login_page')
    else:
        return render(request, 'login.html')    


def hca_signup(request):
    if request.method == "POST":
        # username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role = User.HCA 

        if password == confirm_password:
            # if User.objects.filter(username=username).exists():
            #     # messages.info(request, 'Username already exists')
            #     # return redirect('register')
            #     return render(request, 'signup.html', {'username_exists': True})
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('hca_signup')
            else:
                # user = User.objects.create_user(email=email,password=password)
                user = User.objects.create_user(email=email, password=password, role=role)
                
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login_page')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('hca_signup')
    else:
        return render(request, 'hca_signup.html')



def register(request):
    if request.method == "POST":
        # username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        role=User.PATIENTS

        if password == confirm_password:
            # if User.objects.filter(username=username).exists():
            #     # messages.info(request, 'Username already exists')
            #     # return redirect('register')
            #     return render(request, 'signup.html', {'username_exists': True})
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('register')
            else:
                # user = User.objects.create_user(email=email,password=password)
                user = User.objects.create_user(email=email, password=password, role=role)    
                profile=PatientProfile(user=user,email=email)  
                profile.save()          
                user.save()
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login_page')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('register')
    else:
        return render(request, 'signup.html')




def loggout(request):
        print('Logged Out')
        logout(request)
        return redirect('/')




class ResetPasswordView(SuccessMessageMixin,PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')


def doctor(request):
    
    images = Image.objects.all()

    
    context = {
        'images': images,
    }

    return render(request, 'doctor.html', context)

def edit_gallery(request):
    
    images = Image.objects.all()

    
    context = {
        'images': images,
    }

    return render(request, 'admin_temp/edit_gallery.html', context)

def index(request):
    
    images = Image.objects.all()

    
    context = {
        'images': images,
    }

    return render(request, 'index.html', context)

def ad_gallery(request):
    if request.method == 'POST':
        # Handle form submission for image upload
        title = request.POST['title']
        description = request.POST['description']
        image_file = request.FILES['image']

        # Create a new Image object and save it to the database
        image = Image(title=title, description=description, image=image_file)
        image.save()

        return render(request,'admin_temp/adgallery.html')  # Redirect back to the ad_gallery page after successful image upload

    # Retrieve a list of all images from the database
    images = Image.objects.all()

    # Pass the list of images to the ad_gallery.html template
    context = {
        'images': images,
    }

    return render(request, 'admin_temp/adgallery.html', context)
    
