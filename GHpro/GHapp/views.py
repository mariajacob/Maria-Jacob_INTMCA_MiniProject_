from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Ashaworker,Blog,AshaworkerSchedule,Hca
from .models import Appointment,Slots
from .models import PatientProfile
from .models import MedicalRecord

from .models import Image 
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .decorators import patient_required
from django.shortcuts import render, get_object_or_404, redirect
from .decorators import ashaworker_required
from django.core.mail import send_mail
from io import BytesIO
from django.db.models import Count
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.db.models import Count
from .models import CustomUser


from .models import Ashaworker, PatientProfile, Appointment
from django.utils import timezone
import matplotlib.pyplot as plt
from io import BytesIO
import base64





from django.conf import settings



from django.contrib.auth import get_user_model
# Create your views here.



User=get_user_model()

patient_required
def index(request):
    return render(request,'index.html')

patient_required
def about(request):
    return render(request,'about.html')

patient_required
def treatment(request):
    return render(request,'treatment.html')

patient_required
def testimonial(request):
    return render(request,'testimonial.html')

patient_required
def contact(request):
    return render(request,'contact.html')

def index2(request):
    return render(request,'admin_temp/index-2.html')


def index(request):
    return render(request,'index.html')

def hca_index(request):
    return render(request,'hca_temp/hca_index.html')

def schedule(request):
    # Get all Ashaworkers
    ashaworkers = Ashaworker.objects.all()

    # Create a list to store each Ashaworker's schedule
    schedules = []

    # Get the current date and time
    current_datetime = timezone.now()

    # Iterate through all Ashaworkers and fetch their schedules
    for ashaworker in ashaworkers:
        # Fetch time slots associated with each Ashaworker and filter out past slots
        time_slots = Slots.objects.filter(ashaworker=ashaworker, date__gte=current_datetime)
        
        # Append the Ashaworker and their schedule to the list if they have future slots
        if time_slots.exists():
            schedules.append({
                'ashaworker': ashaworker,
                'time_slots': time_slots,
            })

    return render(request, 'admin_temp/schedule.html', {'schedules': schedules})


# def add_schedule(request):
#     time_slots = []  # Initialize an empty list for time slots
#     if request.method == 'POST':
#         # Get data from the HTML form
#         Name = request.POST['Name']
#         print(Name)
#         available_days = request.POST['available_days']
#         preferred_date = request.POST.get('preferred_date')
#         preferred_time = request.POST.get('preferred_time')

#         try:
#             # Find the Ashaworker by ID
#             # ashaworker = Ashaworker.objects.get(pk=ashaworker_id,Name=Name)
#             ashaworker = Ashaworker.objects.get(Name=Name)
#             # Create a new AshaworkerSchedule instance and save it
#             schedule = AshaworkerSchedule(
#             ashaworker=ashaworker,
#             # Name=Name,
#             available_days=available_days,
#             preferred_date=preferred_date,
#             preferred_time=preferred_time
#             )
#             schedule.save()
#             return redirect('schedule')
#             # return HttpResponse('Schedule created successfully')  # You can customize this response

#         except Ashaworker.DoesNotExist:
#             return HttpResponse('Ashaworker not found')  # You can customize this response
#     else:
#         # Generate time slots with 30-minute intervals for AM and PM
#         start_time = datetime.strptime("06:00 AM", "%I:%M %p")
#         end_time = datetime.strptime("09:00 PM", "%I:%M %p")
#         interval = timedelta(minutes=30)

#         while start_time <= end_time:
#             time_slots.append(start_time.strftime("%I:%M %p"))
#             start_time += interval
#     # Handle GET request (display the form)
#     # You may want to pass a list of Ashaworkers to the template for the dropdown
#     ashaworkers = Ashaworker.objects.all()
#     return render(request, 'admin_temp/add_schedule.html', {'ashaworkers': ashaworkers,'time_slots': time_slots,})


def asha_timeslots(request):
    # Check if a 'Docs' object exists for the logged-in user
    try:
        logged_in_asha = Ashaworker.objects.get(user=request.user)
    except Ashaworker.DoesNotExist:
        # Handle the case where a 'Docs' object does not exist for the logged-in user
        # You can redirect or display an error message as needed
        return render(request, 'error_template.html', {'error_message': 'Ashaworker profile not found'})

    # Extract the doctor's name from the 'Name' attribute of the 'Docs' object
    asha_name = logged_in_asha.Name

    if request.method == 'POST':
        # Retrieve form data from POST request
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time:
            # Create and save the time slot associated with the logged-in doctor
            ashaworker = logged_in_asha  # Use the 'logged_in_doctor' from your previous code
            slot = Slots(ashaworker=ashaworker, date=date, start_time=start_time, end_time=end_time)
            slot.save()

            # Optionally, you can add a success message or redirect to another page
            return render(request, 'asha_temp/asha_timeslots.html', {'asha_name': asha_name, 'success_message': 'Time slot saved successfully'})
        else:
            # Handle the case where 'start_time' is not provided
            # You can render an error message or take appropriate action
            return render(request, 'asha_temp/asha_timeslots.html', {'asha_name': asha_name, 'error_message': 'Please provide a valid start time'})

    # Render the template for both GET and POST requests
    return render(request, 'asha_temp/asha_timeslots.html', {'asha_name': asha_name})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Slots

@login_required
def asha_timeslots_shows(request):
    # Get the logged-in doctor
    logged_in_asha = Ashaworker.objects.get(user=request.user)

    # Fetch time slots associated with the logged-in doctor
    time_slots = Slots.objects.filter(ashaworker=logged_in_asha)

    return render(request, 'asha_temp/asha_timeslots_shows.html', {'time_slots': time_slots})



def resources(request):
    blogs = Blog.objects.all()
    return render(request, 'resources.html', {'blogs': blogs})

def resources_details(request, blog_id):
    # Get the blog instance with the specified blog_id
    blog = get_object_or_404(Blog, id=blog_id)
    
    return render(request, 'resources_details.html', {'blog': blog})


def search_resources(request):
    # Get the search query from the GET request
    search_query = request.GET.get('resourcesname', '')

    # Filter Ashaworkers whose name contains the search query
    blogs = Blog.objects.filter(title__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'blogs': blogs,
        'search_query': search_query,
    }

    return render(request, 'resources.html', context)
 
def blog_details(request, blog_id):
    # Get the blog instance with the specified blog_id
    blog = get_object_or_404(Blog, id=blog_id)
    
    return render(request, 'admin_temp/blog-details.html', {'blog': blog})



def blog(request):
    
    blogs = Blog.objects.all()
    return render(request, 'admin_temp/blog.html', {'blogs': blogs})
     # Retrieve all blog objects from the database
    

def add_blog(request):
    if request.method == 'POST':
        author = request.POST['author']
        title = request.POST['title']
        category = request.POST['category']
        description = request.POST['description']
        blog_date = request.POST['blog_date']
        
        # Handle image upload if needed
        if 'images' in request.FILES:
            images = request.FILES['images']
        else:
            images = None
        
        # Create a new Blog instance
        new_blog = Blog(
            author=author,
            title=title,
            category=category,
            description=description,
            blog_date=blog_date,
            images=images
        )
        
        # Save the new blog entry
        new_blog.save()
        
        return redirect('blog')  # Redirect to a list view of all blogs

    return render(request, 'admin_temp/add-blog.html')


# def edit_blog(request):
#     return render(request,'admin_temp/edit-blog.html')

def edit_blog(request, blog_id):
    # Get the blog instance to be edited
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        # Update the blog instance with the new data
        blog.author = request.POST['author']
        blog.title = request.POST['title']
        blog.category = request.POST['category']
        blog.description = request.POST['description']
        blog.blog_date = request.POST['blog_date']

        # Handle image update if a new image is provided
        if 'images' in request.FILES:
            blog.images = request.FILES['images']

        # Save the updated blog instance
        blog.save()

        # Redirect to the blog detail page or any other desired page
        return redirect('blog')

    return render(request, 'admin_temp/edit-blog.html', {'blog': blog,'blog_id':blog.id})




from .models import Donation
from django.urls import reverse
@login_required(login_url='login_page')
def donation(request):
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name')
        email = request.POST.get('email')
        donor_place = request.POST.get('donor_place')
        amount = request.POST.get('amount')
        message = request.POST.get('message')

        donation = Donation(
            donor_name=donor_name,
            email=email,
            donor_place=donor_place,
            amount=amount,
            message=message
        )
        donation.save()
        return redirect('payment',donat_id=donation.id)

        
       
    return render(request, 'donation.html')  # Replace with your template name



@login_required(login_url='login_page')
def patients(request):
    patients = PatientProfile.objects.filter()
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.all()
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'admin_temp/patients.html', {'patients': patients, 'ward_numbers': ward_numbers})
    # patients = CustomUser.objects.filter(role=CustomUser.PATIENTS)
    # patients = PatientProfile.objects.filter()
    # return render(request, 'admin_temp/patients.html ', {'patients': patients})


from django.contrib.auth.decorators import login_required

@login_required(login_url='login_page')
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

        profile.birth_date = request.POST.get('birth_date')
        print("dob :",profile.birth_date)

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

@login_required(login_url='login_page')
def print_patient_profile(request):
    profile = PatientProfile.objects.filter(user=request.user).first() 
    return render(request, 'print_patient_profile.html', {'profile': [profile]})



@login_required(login_url='login_page')
def edit_asha_pro(request):
    
    # user = request.user
    # profile = PatientProfile.objects.get(user=user)
    user = request.user
    asha = get_object_or_404(Ashaworker, user=user)
    asha = Ashaworker.objects.get(user=user)
    
    if request.method == "POST":
        print ('POST')
        # user.first_name=request.POST.get('first_name')
        # user.last_name=request.POST.get('last_name')
        # Process the form data and save/update the profile

        asha.Name = request.POST.get('name')
        
        asha.email = request.POST.get('email')
       
        asha.gender = request.POST.get('gender')
        

        asha.date_of_birth = request.POST.get('dob')
        

        asha.date_of_join = request.POST.get('doj')
        

        asha.address = request.POST.get('address')
       

        asha.ward = request.POST.get('ward')
        

        asha.postal = request.POST.get('pin')
        

        asha.phone = request.POST.get('phone')
       

        asha.Panchayat = request.POST.get('panchayat')
        

        asha.phone = request.POST.get('phone')

        asha.edu_level = request.POST.get('edu_level')
        asha.edu_inst = request.POST.get('edu_inst')
        asha.year_pass_edu = request.POST.get('year_pass_edu')
        
        asha.add_training = request.POST.get('add_training')
        asha.add_training_inst = request.POST.get('add_training_inst')
        asha.year_pass_add = request.POST.get('year_pass_add')

        new_id_proof = request.FILES.get('id_proof')
        if new_id_proof:
            # Delete the old ID proof if it exists
            if asha.id_proof:
                fs = FileSystemStorage()
                fs.delete(asha.id_proof.name)

            # Save the new ID proof to the 'id_proofs/' directory
            fs = FileSystemStorage()
            filename = fs.save(f"id_proofs/{new_id_proof.name}", new_id_proof)
            asha.id_proof = filename

        new_edu_certificate = request.FILES.get('edu_certificate')
        if new_edu_certificate:
            # Delete the old educational certificate if it exists
            if asha.edu_certificate:
                fs = FileSystemStorage()
                fs.delete(asha.edu_certificate.name)

            # Save the new educational certificate to the 'edu_cert/' directory
            fs = FileSystemStorage()
            filename = fs.save(f"edu_cert/{new_edu_certificate.name}", new_edu_certificate)
            asha.edu_certificate = filename

        new_add_certificate = request.FILES.get('add_certificate')
        if new_add_certificate:
            # Delete the old additional training certificate if it exists
            if asha.add_certificate:
                fs = FileSystemStorage()
                fs.delete(asha.add_certificate.name)

            # Save the new additional training certificate to the 'add_cert/' directory
            fs = FileSystemStorage()
            filename = fs.save(f"add_cert/{new_add_certificate.name}", new_add_certificate)
            asha.add_certificate = filename


        new_profile_pic = request.FILES.get('profile_photo')
        
        if new_profile_pic:
            # Delete the old profile photo if it exists
            if asha.profile_photo:
                fs = FileSystemStorage()
                fs.delete(asha.profile_photo.name)
            
            # Save the new profile photo to a specific directory
            fs = FileSystemStorage()
            filename = fs.save(f"profile_photos/{new_profile_pic.name}", new_profile_pic)
            asha.profile_photo = filename 
        asha.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('pro_ashaworker')  # Redirect to the profile page
    context = {
        'user': user,
        'asha': asha
    }

    return render(request, 'asha_temp/edit_asha_pro.html',context)

@login_required(login_url='login_page')
def pro_ashaworker(request):
    asha = Ashaworker.objects.filter(user=request.user).first() 
    return render(request, 'asha_temp/pro_ashaworker.html', {'asha': [asha]})

from datetime import datetime

from django.utils import timezone
@login_required(login_url='login_page')
def ad_appointment(request):
    current_date = timezone.now().date()
    current_appointments = Appointment.objects.filter(date=current_date).order_by('date', 'slot__start_time')
    future_appointments = Appointment.objects.filter(date__gt=current_date).order_by('date', 'slot__start_time')
    past_appointments = Appointment.objects.filter(date__lt=current_date).order_by('-date', 'slot__start_time')
    
    return render(request, 'admin_temp/appointments.html', {
        'current_appointments': current_appointments,
        'future_appointments': future_appointments,
        'past_appointments': past_appointments,
    })

def current_appointment(request):
    current_date = timezone.now().date()
    current_appointments = Appointment.objects.filter(date=current_date).order_by('date', 'slot__start_time')
    
    
    return render(request, 'admin_temp/current_appointment.html', {
        'current_appointments': current_appointments,
        
    })

def future_appointment(request):
    current_date = timezone.now().date()
    
    future_appointments = Appointment.objects.filter(date__gt=current_date).order_by('date', 'slot__start_time')
    
    
    return render(request, 'admin_temp/future_appointment.html', {
        
        'future_appointments': future_appointments,
        
    })

def past_appointment(request):
    current_date = timezone.now().date()
    
    past_appointments = Appointment.objects.filter(date__lt=current_date).order_by('-date', 'slot__start_time')
    
    return render(request, 'admin_temp/past_appointment.html', {
        
        'past_appointments': past_appointments,
    })


@login_required(login_url='login_page')
def asha_approved_appointments(request):
    # Get the currently logged-in Asha worker
    current_asha_worker = request.user

    # Filter approved appointments based on the logged-in Asha worker's email
    approved_appointments = Appointment.objects.filter(is_approved=True, ashaworker__email=current_asha_worker.email)

    return render(request, 'asha_temp/asha_approved_appo.html', {'approved_appointments': approved_appointments})
# def asha_approved_appointments(request):
#     approved_appointments = Appointment.objects.filter(is_approved=True)
#     print(approved_appointments)
#     return render(request, 'asha_temp/asha_approved_appo.html', {'approved_appointments': approved_appointments})

from django.shortcuts import get_object_or_404, redirect
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.is_approved = True
    appointment.save()
    # messages.success(request, 'Appointment approval successful. An approval email with the login link has been sent to the Patient.')
    return redirect("appointments")

@ashaworker_required
def patient_users(request):
    # patients = CustomUser.objects.filter(role=CustomUser.PATIENTS)
    patients = PatientProfile.objects.filter()
    return render(request, 'asha_temp/patient_users.html', {'patients': patients})

def patients_by_ward(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.all()
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'asha_temp/patients_by_ward.html', {'patients': patients, 'ward_numbers': ward_numbers})





@login_required(login_url='login_page')
def search_patient(request):
    # Get the search query from the GET request
    search_query = request.GET.get('patientname', '')

    # Filter Ashaworkers whose name contains the search query
    patients = PatientProfile.objects.filter(first_name__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'asha_temp/patient_users.html', context)


@login_required(login_url='login_page')
def appointment_form(request, appointment_id=None):
    patientprofile = request.user.patientprofile
    ashaworkers = Ashaworker.objects.all()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        ward_asha = request.POST.get('ward')
        phone_number = request.POST.get('phone_number')
        medical_conditions = request.POST.get('medical_conditions')
        urgency = request.POST.get('urgency')
        medication_names = request.POST.get('medication_names')
        symptoms = request.POST.get('symptoms')
        asha_id = request.POST.get('ashaworker')
        date_id = request.POST.get('date')
        selected_time_slot = request.POST.get('time')

        try:
            slot = Slots.objects.get(id=selected_time_slot)
            ashaworker = Ashaworker.objects.get(id=asha_id)
            user = CustomUser.objects.get(id=request.user.id)

            appointment = Appointment(
                first_name=first_name,
                last_name=last_name,
                email=email,
                gender=gender,
                address=address,
                ward_asha=ward_asha,
                phone_number=phone_number,
                medical_conditions=medical_conditions,
                urgency=urgency,
                medication_names=medication_names,
                symptoms=symptoms,
                ashaworker=ashaworker,
                user=user,
                slot=slot,
                date=date_id,
                status=False
            )
            appointment.save()
            subject = 'Appointment is Successful'
            message = f'Your appointment for home visit is successful. Your Scheduled date: {date_id}, Your Scheduled Time: {selected_time_slot}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)

        except Slots.DoesNotExist:
            return render(request, 'appointment.html', {'error_message': 'Time slot not found'})
        except ValueError:
            return render(request, 'appointment.html', {'error_message': 'Invalid time format'})

    return render(request, 'appointment.html', {'patientprofile': patientprofile, 'appointment_id': appointment_id,'ashaworkers': ashaworkers})


def get_dates_for_ashaworker(request):
    ashaworker_id = request.GET.get('ashaworker_id')
    try:
        ashaworker = Ashaworker.objects.get(id=ashaworker_id)
        slots = Slots.objects.filter(ashaworker=ashaworker)
        date_options = [slot.date.strftime('%Y-%m-%d') for slot in slots]
        return JsonResponse({'date_options': date_options})
    except Ashaworker.DoesNotExist:
        return JsonResponse({'error_message': 'Ashaworker not found'})

@login_required
def get_timeslots_for_date(request):
    ashaworker_id = request.GET.get('ashaworker_id')
    selected_date = request.GET.get('selected_date')

    try:
        ashaworker = Ashaworker.objects.get(id=ashaworker_id)
        slots = Slots.objects.filter(ashaworker=ashaworker, date=selected_date)
        time_options = [{'id': slot.id, 'text': f'{slot.start_time.strftime("%I:%M %p")} - {slot.end_time.strftime("%I:%M %p")}'}
                        for slot in slots]
        return JsonResponse({'time_options': time_options})
    except Ashaworker.DoesNotExist:
        return JsonResponse({'error_message': 'Ashaworker not found'})

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

def check_ward_exists(request):
    ward = request.GET.get("ward", "")
    ward_exists = Ashaworker.objects.filter(ward=ward).exists()
    response_data = {"exists": ward_exists}
    return JsonResponse(response_data)


def add_asha(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
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
        profile_photo = request.FILES.get('profile_photo')
        role = CustomUser.ASHAWORKER
        print(role)

        # Check if a user with the same email and role exists
        if CustomUser.objects.filter(email=email, role=CustomUser.ASHAWORKER).exists():
            messages.info(request, 'Email already exists')
            return redirect('add_asha')

        # Check if a user with the same ward exists
        if Ashaworker.objects.filter(ward=ward).exists():
            messages.info(request, 'Ward already assigned to another Ashaworker')
            return redirect('add_asha')

        # Create the user and Ashaworker records
        user = CustomUser.objects.create_user(email=email, password=password)
        user.role = CustomUser.ASHAWORKER
        user.save()
        asha = Ashaworker(user=user, Name=name, email=email, date_of_birth=dob, date_of_join=doj,
                         gender=gender, address=address, taluk=taluk, Panchayat=panchayat, ward=ward,
                         postal=pin, phone=phone, profile_photo=profile_photo)
        asha.save()

        subject = 'Ashaworker Login Details'
        message = f'Registered as an Ashaworker. Your username: {email}, Password: {password}'
        from_email = settings.EMAIL_HOST_USER  # Your email address
        recipient_list = [user.email]  # Employee's email address

        send_mail(subject, message, from_email, recipient_list)

        return redirect('ad_ashaworker')
    else:
        return render(request, 'admin_temp/add_asha.html')



@login_required(login_url='login_page')
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
        new_profile_photo = request.FILES.get('new_profile_photo')
        if new_profile_photo:
            ashaworker.profile_photo = new_profile_photo

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


@login_required(login_url='login_page')
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


@login_required(login_url='login_page')
def admin_dashboard(request):
    # Get the current date and time
    current_date = timezone.now().date()

    # Retrieve Asha Workers
    ashaworkers = Ashaworker.objects.all()

    # Retrieve Patients
    patients = PatientProfile.objects.all()
    appointments = Appointment.objects.all()
    
    approved_appointments = Appointment.objects.filter(is_approved=True)


    # Query the database to count the number of appointments for each patient
    appointments_count = Appointment.objects.values('user__email').annotate(appointment_count=Count('id'))

    # Extract the patient usernames and appointment counts for the chart
    patient_usernames = [appointment['user__email'] for appointment in appointments_count]
    appointment_counts = [appointment['appointment_count'] for appointment in appointments_count]

    ashaworkers = Ashaworker.objects.annotate(appointment_count=Count('appointments'))
    ashaworker_count = ashaworkers.count()
    patients_count = patients.count()
    appointments_count = appointments.count()
    approved_appointments=approved_appointments.count()
    # Create a DataFrame to store the data
    data = {
        'Ashaworker': [worker.Name for worker in ashaworkers],
        'Appointment Count': [worker.appointment_count for worker in ashaworkers],
    }

    # Convert the data to a DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Create a line chart
    plt.figure(figsize=(6, 4))
    plt.plot(data['Ashaworker'], data['Appointment Count'], marker='o', linestyle='-', color='b')
    plt.title('Ashaworker Appointment Count')
    plt.xlabel('Ashaworker')
    plt.ylabel('Appointment Count')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the plot to base64 for embedding in the HTML template
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'admin_temp/adindex.html', {
        'ashaworkers': ashaworkers,
        'patients': patients,
        'patient_usernames': patient_usernames,
        'appointment_counts': appointment_counts,
        'current_date': current_date,
        'plot_data': plot_data,
        'ashaworker_count': ashaworker_count,
        'patients_count': patients_count,
        'appointments_count': appointments_count,
        'approved_appointments': approved_appointments,
        
        
    })



@ashaworker_required
def asha_index(request):

    return render(request, 'asha_temp/asha_index.html')

@ashaworker_required
def asha_profile(request):
     
    return render(request, 'asha_temp/asha_profile.html')


def login_page(request):
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
                return redirect('hca_index')
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


# def hca_signup(request):
#     if request.method == "POST":
#         # username = request.POST['email']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirmPassword']
#         role = User.HCA 

#         if password == confirm_password:
#             # if User.objects.filter(username=username).exists():
#             #     # messages.info(request, 'Username already exists')
#             #     # return redirect('register')
#             #     return render(request, 'signup.html', {'username_exists': True})
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email already exists') 
#                 return redirect('hca_signup')
#             else:
#                 # user = User.objects.create_user(email=email,password=password)
#                 user = User.objects.create_user(email=email, password=password, role=role)
                
#                 user.save()
#                 messages.success(request, 'Registration successful. You can now log in.')
#                 return redirect('login_page')
#         else:
#             messages.error(request, 'Password confirmation does not match')
#             return redirect('hca_signup')
#     else:
#         return render(request, 'hca_signup.html')



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
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists') 
                return redirect('register')
            else:
                # user = User.objects.create_user(email=email,password=password)
                user = CustomUser.objects.create_user(email=email, password=password, role=role)    
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


def gallery(request):
    
    images = Image.objects.all()

    
    context = {
        'images': images,
    }

    return render(request, 'doctor.html', context)

@login_required(login_url='login_page')
def dis_gallery(request):
    # Retrieve a list of enabled images from the database
    images = Image.objects.filter(is_enabled=True)

    context = {
        'images': images,
    }

    return render(request, 'admin_temp/edit_gallery.html', context)
# def dis_gallery(request):
    
#     images = Image.objects.all()

    
#     context = {
#         'images': images,
#     }

#     return render(request, 'admin_temp/edit_gallery.html', context)

def index(request):
    
    images = Image.objects.all()

    
    context = {
        'images': images,
    }

    return render(request, 'index.html', context)

def edit_gallery_image(request):
    return render(request,'admin_temp/edit_gallery_images.html')

@login_required(login_url='login_page')
def ad_gallery(request):
    if request.method == 'POST':
        # Handle form submission for image upload
        title = request.POST['title']
        description = request.POST['description']
        image_file = request.FILES['image']

        # Create a new Image object and save it to the database
        image = Image(title=title, description=description, image=image_file)
        image.save()

        return redirect('dis_gallery')  # Redirect back to the ad_gallery page after successful image upload

    # Retrieve a list of all images from the database
    images = Image.objects.all()

    # Pass the list of images to the ad_gallery.html template
    context = {
        'images': images,
    }

    return render(request, 'admin_temp/adgallery.html', context)


def edit_gallery_images(request, image_id):
    # Get the image object to edit
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        # Handle form submission for image edit
        title = request.POST['title']
        description = request.POST['description']

        # Update the image object
        image.title = title
        image.description = description

        # Handle updating the image file if a new file is provided
        if 'image' in request.FILES:
            new_image = request.FILES['image']
            image.image = new_image

        image.save()

        return redirect('dis_gallery')  # Redirect back to the image display page after successful edit

    context = {
        'image': image,
    }

    return render(request, 'admin_temp/edit_gallery_images.html', context)

def soft_delete_image(request, image_id):
    # Get the image object to soft delete
    image = get_object_or_404(Image, id=image_id)

    # Soft delete the image by setting is_enabled to False
    image.is_enabled = False
    image.save()

    return redirect('dis_gallery')

from django.http import HttpResponse
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment(request, donat_id):
    donation = Donation.objects.get(pk=donat_id)

    currency = 'INR'
    amount = donation.amount
    amount_in_paise = int(amount * 100)

    # Create a Razorpay client instance using your API credentials
    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'  # Payment capture should be '0' for manual capture
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'  # You can specify your callback URL

    # Pass these details to the frontend
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context=context)

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@csrf_exempt
def paymenthandler(request):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is not None:
            try:
                # Retrieve the authorized amount from the Razorpay order
                razorpay_order = razorpay_client.order.fetch(razorpay_order_id)
                authorized_amount = razorpay_order['amount']

                # Capture the payment with the authorized amount
                razorpay_client.payment.capture(payment_id, authorized_amount)

                # Payment capture successful.
                return render(request, 'index.html')  # Replace 'about.html' with your actual success page template
            except razorpay.errors.BadRequestError as e:
                # Handle the error appropriately, e.g., show an error message to the user.
                return HttpResponse("Payment capture failed: " + str(e), status=400)

    return HttpResponse(status=400)

@login_required
def medical_record(request, patient_id):
    # Retrieve the patient based on the patient_id
    try:
        patient = PatientProfile.objects.get(pk=patient_id)
    except PatientProfile.DoesNotExist:
        return HttpResponse("Patient not found", status=404)

    if request.method == "POST":
        # Get the data from the form
        date = request.POST.get("date")
        # first_name = request.POST.get("first_name")
        # last_name = request.POST.get("last_name")
        doctor_notes = request.POST.get("doctor_notes")
        medications_needed = request.POST.get("medications_needed")
        treatments = request.POST.get("treatments")
        current_conditions = request.POST.get("current_conditions")

        # Create a new MedicalRecord object with the associated patient
        # You need to ensure that user field receives a CustomUser instance
        # Assuming that patient.user is the related CustomUser instance
        MedicalRecord.objects.create(
            user=patient.user,
            date=date,
            # first_name=first_name,
            # last_name=last_name,
            doctor_notes=doctor_notes,
            medications_needed=medications_needed,
            treatments=treatments,
            current_conditions=current_conditions,
        )

        return redirect("medical_record_display")

    return render(request, "medical_record.html", {"patient": patient})


@login_required
def medical_record_search(request):
    if request.method == 'GET':
        selected_date = request.GET.get('selected_date')

        if selected_date:
            medical_record = MedicalRecord.objects.filter(user=request.user, date=selected_date).order_by('-date')
        else:
            medical_record = MedicalRecord.objects.filter(user=request.user).order_by('-date')

        return render(request, "medical_record_display.html", {"medical_record": medical_record})

@login_required
def medical_record_display(request):
    medical_record = MedicalRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "medical_record_display.html", {"medical_record": medical_record})

from django.http import HttpResponse, FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

def generate_medical_record_pdf(request):
    # Get the logged-in user's medical records
    medical_records = MedicalRecord.objects.filter(user=request.user).order_by('-date')

    # Retrieve the patient's first name and last name
    patient_profile = request.user.patientprofile  # Assuming you have a one-to-one relationship
    first_name = patient_profile.first_name
    last_name = patient_profile.last_name
    # Get the user's full name

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file."
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold the data for the table
    data = [["Date", "Doctor's Notes", "Medications Needed", "Treatments", "Current Conditions"]]

    # Populate the data list with medical record information
    for record in medical_records:
        data.append([
            str(record.date),
            record.doctor_notes,
            record.medications_needed,
            record.treatments,
            record.current_conditions
        ])

    # Create a table style and apply it to the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    table = Table(data)
    table.setStyle(table_style)

    # Create a Paragraph for the heading and the user's name
    styles = getSampleStyleSheet()
    main_heading_style = ParagraphStyle(
        name='MainHeadingStyle',
        parent=styles['Heading1'],
        alignment=1  # Center alignment
    )
    main_heading_text = Paragraph("<b>Gentle Haloes Palliative Care</b>", main_heading_style)
    
    sub_heading_style = ParagraphStyle(
        name='SubHeadingStyle',
        parent=styles['Heading2'],
        alignment=1  # Center alignment
    )
    sub_heading_text = Paragraph("<b>Parathodu Grama Panchayath</b>", sub_heading_style)

    sub_heading_medical_record = Paragraph("<b>Medical Record</b>", sub_heading_style)  # Converted to subheading

    user_name_text = Paragraph("<b>Patient Name:</b> {} {}".format(first_name, last_name), styles['Normal'])

    # Build the PDF document with the desired structure and reduced spacing
    elements = [main_heading_text, sub_heading_text, Spacer(1, 5), sub_heading_medical_record, Spacer(1, 5), user_name_text, Spacer(1, 10), table]
    pdf.build(elements)

    # Move the buffer position to the beginning
    buffer.seek(0)

    # Create a response with the PDF data
    response = FileResponse(buffer, as_attachment=True, filename="medical_record.pdf")

    return response

  # Import the User model

def appointment_chart(request):
    # Query the database to count the number of appointments for each patient
    appointments_count = Appointment.objects.values('user__email').annotate(appointment_count=Count('id'))

    # Extract the patient usernames and appointment counts for the chart
    patient_usernames = [appointment['user__email'] for appointment in appointments_count]
    appointment_counts = [appointment['appointment_count'] for appointment in appointments_count]

    return render(request, 'admin_temp/appointment_chart.html', {'patient_usernames': patient_usernames, 'appointment_counts': appointment_counts})






def ashaworker_appointment_chart(request):
    # Get the Ashaworkers and their associated appointment counts
    ashaworkers = Ashaworker.objects.annotate(appointment_count=Count('appointments'))

    # Create a DataFrame to store the data
    data = {
        'Ashaworker': [worker.Name for worker in ashaworkers],
        'Appointment Count': [worker.appointment_count for worker in ashaworkers],
    }

    # Convert the data to a DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Create a line chart
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(df['Ashaworker'], df['Appointment Count'], marker='o', linestyle='-', color='b')
    plt.title('Ashaworker Appointment Count')
    plt.xlabel('Ashaworker')
    plt.ylabel('Appointment Count')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()

    # Save the plot to a BytesIO object
    from io import BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the plot to base64 for embedding in the HTML template
    import base64
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'admin_temp/appointment_chart1.html', {'plot_data': plot_data})

def add_hca(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        hcaname = request.POST.get('hcaname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        date_of_join = request.POST.get('date_of_join')
        
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        
        postal = request.POST.get('postal')
        phone = request.POST.get('phone')
        profile_photo = request.FILES.get('profile_photo')
        license_certificate=request.FILES.get('license_certificate')
        year_hca=request.FILES.get('year_hca')
        role = CustomUser.HCA
        print(role)

        # Check if a user with the same email and role exists
        if CustomUser.objects.filter(email=email, role=CustomUser.HCA).exists():
            messages.info(request, 'Email already exists')
            return redirect('add_hca')

        # Check if a user with the same ward exists
        

        # Create the user and Ashaworker records
        user = CustomUser.objects.create_user(email=email, password=password)
        user.role = CustomUser.HCA
        user.save()
        hca = Hca(user=user, hcaname=hcaname, email=email,date_of_join=date_of_join,
                         address=address, taluk=taluk, panchayat=panchayat,
                         postal=postal, phone=phone, profile_photo=profile_photo,license_certificate=license_certificate,year_hca=year_hca)
        hca.save()

        subject = 'Hospital Login Details'
        message = f'Registered as an Hospital. Your username: {email}, Password: {password}'
        from_email = settings.EMAIL_HOST_USER  # Your email address
        recipient_list = [user.email]  # Employee's email address

        send_mail(subject, message, from_email, recipient_list)

        return redirect('ad_hca')
    else:
        return render(request, 'admin_temp/add_hca.html')
    
@login_required(login_url='login_page')
def edit_hca(request, hca_id):
    hca = get_object_or_404(Hca, id=hca_id)
    if request.method == 'POST':
        hcaname = request.POST.get('hcaname')
        email = request.POST.get('email')
        password=request.POST.get('password')
        
        date_of_join = request.POST.get('date_of_join')
        
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
       
        postal = request.POST.get('postal')
        phone = request.POST.get('phone')
        
        year_hca=request.FILES.get('year_hca')
        new_profile_photo = request.FILES.get('new_profile_photo')
        if new_profile_photo:
            hca.profile_photo = new_profile_photo
        
        new_li_photo = request.FILES.get('new_li_photo')
        if new_li_photo:
            hca.license_certificate = new_li_photo

        hca.hcaname = hcaname
        hca.email = email
        hca.set_password(password)
        
        hca.date_of_join = date_of_join
        
        hca.address = address
        hca.taluk = taluk
        hca.panchayat = panchayat
        
        hca.postal = postal
        hca.phone = phone
        
        hca.year_hca = year_hca
        hca.save()
        return redirect('ad_hca')
    return render(request, 'admin_temp/edit_hca.html', {'hca': hca})

@login_required(login_url='login_page')
def ad_hca(request):
    hca = Hca.objects.all()
    return render(request, 'admin_temp/ad_hca.html', {'hca': hca})

