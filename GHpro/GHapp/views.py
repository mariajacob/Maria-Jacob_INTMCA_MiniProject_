from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Ashaworker,Nurse,Prescription_model,Member,Panchayath_Ward,Blog,AshaworkerSchedule,Hca,Medicine,MedicineCategory
from .models import Appointment,Slots
from .models import PatientProfile,home_visit
from .models import MedicalRecord,Ashaworker
from .models import Image ,Leave
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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Slots
from .models import Donation
from .models import Member
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

User=get_user_model()


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
    # Filter out only active patients
    patients = PatientProfile.objects.filter(is_active=True)
    ashaworkers = Ashaworker.objects.all()
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = patients.filter(ward=ward_filter)
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'admin_temp/patients.html', {'patients': patients, 'ward_numbers': ward_numbers,'ashaworkers': ashaworkers})


def delete_patients(request, patient_id):
    patients = get_object_or_404(PatientProfile, id=patient_id)

    if request.method == 'POST':
        # Set the is_active attribute to False instead of deleting
        patients.is_active = False
        patients.save()

        # Add a success message to the session
        request.session['deleted_asha_success'] = True

        # Redirect to the 'ad_ashaworker' page (or adjust the URL as needed)
        return redirect('patients')
        
    return render(request, 'admin_temp/delete_patients.html', {'patients': patients})






@login_required(login_url='login_page')
def edit_patient_profile(request):
    
    
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
        print("address :",profile.address)

        profile.birth_date = request.POST.get('birth_date')
        print("dob :",profile.birth_date)

        profile.panchayath= request.POST.get('panchayat')


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
        'profile': profile,
        # 'panchyath_names': panchyath_names,
    }

    return render(request, 'edit_patient_profile.html',context) 

@login_required(login_url='login_page')
def print_patient_profile(request):
    profile = PatientProfile.objects.get(user=request.user)
    ward = profile.ward
    print(ward)
    
    return render(request, 'print_patient_profile.html', {'profile': profile})


from django.contrib.auth import update_session_auth_hash
@login_required(login_url='login_page')
def edit_asha_pro(request):
    
    # user = request.user
    # profile = PatientProfile.objects.get(user=user)
    user = request.user
    asha = get_object_or_404(Ashaworker, user=user)
    asha = Ashaworker.objects.get(user=user)
    
    if request.method == "POST":
        print ('POST')
       

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

        reset_password = request.POST.get('reset_password')
        old_password = request.POST.get('old_password')


        if old_password and reset_password and request.POST.get('cpass') == reset_password:
            if user.check_password(old_password):
                # The old password is correct, set the new password
                user.set_password(reset_password)
                user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
            else:
                messages.error(request, "Incorrect old password. Password not updated.")
        else:
            print("Please fill all three password fields correctly.")
        
        asha.reset_password = reset_password
         

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


@login_required(login_url='login_page')
def appointment_form(request, appointment_id=None):
    patientprofile = request.user.patientprofile
    nurse = Nurse.objects.filter(wardnurse=patientprofile.ward).first()
    ashaworker = Ashaworker.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        ward = request.POST.get('ward')
        phone_number = request.POST.get('phone_number')
        medical_conditions = request.POST.get('medical_conditions')
        urgency = request.POST.get('urgency')
        medication_names = request.POST.get('medication_names')
        symptoms = request.POST.get('symptoms')
        asha_id = request.POST.get('ashaworker')
        date_id = request.POST.get('date')
        selected_time_slot = request.POST.get('time')

        try:
            # Fetching the Nurse object associated with the patient's ward
            
            
            # Fetching other required objects
            slot = Slots.objects.get(id=selected_time_slot)
            ashaworker = Ashaworker.objects.get(id=asha_id)
            user = CustomUser.objects.get(id=request.user.id)

            # Creating the appointment object after all required objects are fetched
            appointment = Appointment(
                first_name=first_name,
                last_name=last_name,
                email=email,
                gender=gender,
                address=address,
                ward=ward,
                phone_number=phone_number,
                medical_conditions=medical_conditions,
                urgency=urgency,
                medication_names=medication_names,
                symptoms=symptoms,
                ashaworker=ashaworker,
                nurse=nurse,  # Assigning the Nurse object to the appointment
                user=user,
                slot=slot,
                date=date_id,
            )
            appointment.save()  # Save the appointment object
            
            # Other existing code...
            subject = 'Appointment is Successful'
            message = f'Your appointment for home visit is successful. Wait for the appointment approval message. Once the appointments is approved the you will get an approval message. Your Scheduled date: {date_id}, Your Scheduled Time: {slot.start_time} {slot.end_time}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('appointment_view')
       
        except Slots.DoesNotExist:
            return render(request, 'appointment.html', {'error_message': 'Time slot not found'})
        except ValueError:
            return render(request, 'appointment.html', {'error_message': 'Invalid time format'})

    return render(request, 'appointment.html', {'patientprofile': patientprofile, 'appointment_id': appointment_id, 'ashaworker': ashaworker, 'nurse': nurse})


def get_times(request):
    selected_date_str = request.GET.get('selected_date', None)
    
    if selected_date_str:
        # Convert the string date to a datetime object
        try:
            selected_date = datetime.strptime(selected_date_str, '%b. %d, %Y').date()
        except ValueError:
            return JsonResponse({'times': []})
        
        # Query the database to get times for the selected date
        slots = Slots.objects.filter(date=selected_date)
        times = [f"{slot.start_time.strftime('%H:%M:%S')} - {slot.end_time.strftime('%H:%M:%S')}" for slot in slots]
        return JsonResponse({'times': times})
    else:
        return JsonResponse({'times': []})


from datetime import datetime
from django.utils import timezone
@login_required(login_url='login_page')
def ad_appointment(request):
    current_date = timezone.now().date()
    
    # Filter out canceled appointments by excluding those with status=False
    current_appointments = Appointment.objects.filter(date=current_date, status=True).order_by('date', 'slot__start_time')
    future_appointments = Appointment.objects.filter(date__gt=current_date, status=True).order_by('date', 'slot__start_time')
    past_appointments = Appointment.objects.filter(date__lt=current_date, status=True).order_by('-date', 'slot__start_time')
    
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




# @login_required(login_url='login_page')
# def nurse_approved_appointments(request):
#     # Get the currently logged-in Asha worker
#     current_nurse = request.user

#     # Filter approved appointments based on the logged-in Asha worker's email
#     approved_appointments = Appointment.objects.filter(is_approved=True, nurse__email=current_nurse.email)

#     return render(request, 'nurse_temp/nurse_approved_appo.html', {'approved_appointments': approved_appointments})



from django.shortcuts import get_object_or_404, redirect
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.is_approved = True
    appointment.save()
    subject = 'Appointment is Successful'
    message = f'Your appointment for home visit is approved.Your Scheduled date: {appointment.date}, Your Scheduled Time: {appointment.slot.start_time} {appointment.slot.end_time}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email]
    send_mail(subject, message, from_email, recipient_list)
    # messages.success(request, 'Appointment approval successful. An approval email with the login link has been sent to the Patient.')
    return redirect("appointments")

@ashaworker_required
def patient_users(request):
    ashaworker = Ashaworker.objects.get(user=request.user)
    ward = ashaworker.ward
    patients = PatientProfile.objects.filter(ward=ward, is_active=True)
    return render(request, 'asha_temp/patient_users.html', {'patients': patients})

def patients_by_ward(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.all()
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'asha_temp/patients_by_ward.html', {'patients': patients, 'ward_numbers': ward_numbers})

def add_view_rec(request):
   
    ashaworker = Ashaworker.objects.get(user=request.user)
    ward = ashaworker.ward
    
    patients = PatientProfile.objects.filter(ward=ward, is_active=True)
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'asha_temp/add_view_rec.html', {'patients': patients, 'ward_numbers': ward_numbers})



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



from django.http import JsonResponse
from datetime import datetime


from django.db.models import Subquery, OuterRef

def get_dates_for_ashaworker(request):
    ashaworker_id = request.GET.get('ashaworker_id')
    
    try:
        ashaworker = Ashaworker.objects.get(id=ashaworker_id)
        
        # Get all available date options for the specific Ashaworker
        slots = Slots.objects.filter(ashaworker=ashaworker).values_list('date', flat=True).distinct()
        date_options = [slot.strftime('%Y-%m-%d') for slot in slots]
        print('ok', date_options)
        
        # Get the selected dates for the Ashaworker from previous appointments
        selected_dates = Appointment.objects.filter(
            ashaworker=ashaworker,
            date__in=date_options,
        ).values_list('date', flat=True)
        print('seected_dates', selected_dates)
        
        # Filter out dates that have been assigned to other patients for the same Ashaworker
        other_patients_selected_dates = Appointment.objects.filter(date__in=date_options, ashaworker_id=ashaworker_id).values_list('date', flat=True)
        print('other seected_dates', other_patients_selected_dates)
        
        date_options = list(filter(lambda date: date not in other_patients_selected_dates, date_options))
        print('dates', date_options)

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


#add panchayath and ward
def add_panward(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        panchayath = request.POST.get('panchayath')
        ward = request.POST.get('ward')
        pan = Panchayath_Ward(panchayath=panchayath,ward=ward)
        pan.save()


        return redirect('ad_panward')
    else:
        return render(request, 'admin_temp/add_panward.html')

from django.http import JsonResponse

def get_wards(request):
    selected_panchayat = request.GET.get('panchayat')
    wards = Panchayath_Ward.objects.filter(panchayath=selected_panchayat).values_list('ward', flat=True)
    return JsonResponse({'wards': list(wards)})

# def get_wards_mem(request):
    selected_panchayat = request.GET.get('panchayat')
    wards = Panchayath_Ward.objects.filter(panchayath=selected_panchayat).values_list('wardmem', flat=True)
    return JsonResponse({'wards': list(wards)})

@login_required(login_url='login_page')
def ad_panward(request):
    panchayaths = Panchayath_Ward.objects.values_list('panchayath', flat=True).distinct()
    
    if request.method == 'GET' and 'panchayath_search' in request.GET:
        panchayath_search = request.GET.get('panchayath_search')
        pan = Panchayath_Ward.objects.filter(panchayath__icontains=panchayath_search)
    else:
        pan = Panchayath_Ward.objects.all()

    return render(request, 'admin_temp/ad_panward.html', {'pan': pan, 'panchayaths': panchayaths})



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

#edit member
    
@login_required(login_url='login_page')
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        wardmem = request.POST.get('wardmem')
        
        phone = request.POST.get('phone')
        new_profile_photo = request.FILES.get('new_profile_photo')
        if new_profile_photo:
            member.profile_photo = new_profile_photo
        member.Name = name
        member.email = email
        member.set_password(password)
        
        member.gender = gender
        member.address = address
        member.taluk = taluk
        member.Panchayat = panchayat
        member.wardmem = wardmem
        
        member.phone = phone
        member.save()
        return redirect('ad_member')
    return render(request, 'admin_temp/edit_member.html', {'member': member})

from django.db.models import Count

@login_required(login_url='login_page')
def ad_ashaworker(request):
    # Retrieve the unique Panchayath values from the Ashaworker model
    unique_panchayaths = Ashaworker.objects.values_list('Panchayat', flat=True).distinct()

    # Retrieve the search parameter from the request
    search_query = request.GET.get('panchayath')

    # Retrieve all Ashaworkers if no search parameter is provided
    if not search_query:
        ashaworkers = Ashaworker.objects.all()
    else:
        # Filter Ashaworkers based on the search parameter (panchayath)
        ashaworkers = Ashaworker.objects.filter(Panchayat__icontains=search_query)

    return render(request, 'admin_temp/ad_ashaworker.html', {'ashaworkers': ashaworkers, 'unique_panchayaths': unique_panchayaths})
    
    

def ad_ashaworker(request):
    # Retrieve the unique Panchayath values from the Ashaworker model
    unique_panchayaths = Ashaworker.objects.values_list('Panchayat', flat=True).distinct()

    # Retrieve the search parameter from the request
    search_query = request.GET.get('panchayath')

    # Retrieve all Ashaworkers if no search parameter is provided
    if not search_query:
        ashaworkers = Ashaworker.objects.all()
    else:
        # Filter Ashaworkers based on the search parameter (panchayath)
        ashaworkers = Ashaworker.objects.filter(Panchayat__icontains=search_query)

    return render(request, 'admin_temp/ad_ashaworker.html', {'ashaworkers': ashaworkers, 'unique_panchayaths': unique_panchayaths})



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


# add Nurse

def add_nurse(request):
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
        wardnurse = request.POST.get('wardnurse')
        
        phone = request.POST.get('phone')
        # profile_photo = request.FILES.get('profile_photo')
        role = CustomUser.NURSE
        print(role)

        # Check if a user with the same email and role exists
        if CustomUser.objects.filter(email=email, role=CustomUser.NURSE).exists():
            messages.info(request, 'Email already exists')
            return redirect('add_nurse')

        # Check if a user with the same ward exists
        if Nurse.objects.filter(wardnurse=wardnurse).exists():
            messages.info(request, 'Ward already assigned to another Nurse')
            return redirect('add_nurse')

        # Create the user and Ashaworker records
        user = CustomUser.objects.create_user(email=email, password=password)
        user.role = CustomUser.NURSE
        user.save()
        nurses = Nurse(user=user, Name=name, email=email, date_of_birth=dob, date_of_join=doj,
                         gender=gender, address=address, taluk=taluk, Panchayat=panchayat, wardnurse=wardnurse,
                         phone=phone)
        nurses.save()

        subject = 'Nurse Login Details'
        message = f'Registered as an Nurse. Your username: {email}, Password: {password}'
        from_email = settings.EMAIL_HOST_USER  # Your email address
        recipient_list = [user.email]  # Employee's email address

        send_mail(subject, message, from_email, recipient_list)

        return redirect('ad_nurse')
    else:
        return render(request, 'admin_temp/add_nurse.html')

# print Nurse
@login_required(login_url='login_page')
def ad_nurse(request):
    # Retrieve the unique Panchayath values from the Ashaworker model
    unique_panchayaths = Nurse.objects.values_list('Panchayat', flat=True).distinct()

    # Retrieve the search parameter from the request
    search_query = request.GET.get('panchayath')

    # Retrieve all Ashaworkers if no search parameter is provided
    if not search_query:
        nurses = Nurse.objects.all()
    else:
        # Filter Ashaworkers based on the search parameter (panchayath)
        nurses = Nurse.objects.filter(Panchayat__icontains=search_query)

    return render(request, 'admin_temp/ad_nurse.html', {'nurses': nurses, 'unique_panchayaths': unique_panchayaths})

# nurse index
#index page of member
def nurse_index(request):
    current_date = timezone.now().date()

    # Retrieve Asha Workers
    ashaworkers = Ashaworker.objects.all()

    # Retrieve Patients
    patients = PatientProfile.objects.all()
    appointments = Appointment.objects.all()
    
    approved_appointments = Appointment.objects.filter(is_approved=True)
    future_appointments = Appointment.objects.filter(date__gt=current_date, status=True).order_by('date', 'slot__start_time')

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

    return render(request, 'nurse_temp/nurse_index.html', {
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

# patient list in nurs index
@login_required
def patient_list_nurse(request):
    # Retrieve the member associated with the logged-in user
    nurse = Nurse.objects.get(user=request.user)
    
    ward_filter = nurse.wardnurse  # Assuming wardmem is the field containing the member's ward
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.none()  # Return an empty queryset
    
    # Assuming you want to display all available ward numbers for the member
    ward_numbers = PatientProfile.objects.filter(ward=ward_filter).values_list('ward', flat=True).distinct()
    
    return render(request, 'nurse_temp/patient_list_nurse.html', {'patients': patients, 'ward_numbers': ward_numbers})


from django.shortcuts import render, redirect
from .models import Prescription_model

from .models import PatientProfile, Medicine, Nurse

@login_required
def add_prescription(request):
    if request.method == 'POST':
        # Get data for each medicine
        medicines = request.POST.getlist('medicines')
        date_of_prescription = request.POST.get('date_of_prescription')

        # Your existing logic to get patient and nurse remains the same
        patient_id = request.POST.get('patient_id')
        patient = PatientProfile.objects.get(id=patient_id)
        nurse = Nurse.objects.get(user=request.user)

        # Loop through selected medicines
        for medicine_id in medicines:
            morning = request.POST.get(f'morning_{medicine_id}')
            noon = request.POST.get(f'noon_{medicine_id}')
            evening = request.POST.get(f'evening_{medicine_id}')
            quantity = request.POST.get(f'quantity_{medicine_id}')
            duration = request.POST.get(f'duration_{medicine_id}')
            dosages = request.POST.get(f'dosages_{medicine_id}')

            # Create prescription for each selected medicine
            prescription = Prescription_model.objects.create(
                nurses=nurse,
                patient=patient,
                medicine=Medicine.objects.get(id=medicine_id),
                morning=morning,
                noon=noon,
                evening=evening,
                date_of_prescription=date_of_prescription,
                quantity=quantity,
                duration=duration,
                dosages=dosages
            )

        return redirect('view_prescription_nurse')

    else:
        # Handle GET request
        # Fetch necessary data for rendering the form
        nurse = Nurse.objects.get(user=request.user)
        patients = PatientProfile.objects.filter(ward=nurse.wardnurse)
        medicines = Medicine.objects.all()

        return render(request, 'nurse_temp/add_prescription.html', {'nurse_name': nurse.Name, 'patients': patients, 'medicines': medicines})



from django.shortcuts import render
from .models import Prescription_model
def view_prescription_nurse(request):
    nurse = Nurse.objects.get(user=request.user)
    patients = set(Prescription_model.objects.filter(nurses=nurse).values_list('patient', flat=True))
    patient_prescriptions = []
    show_latest = request.GET.get('show_latest')
    show_previous = request.GET.get('show_previous')
    
    for patient_id in patients:
        if show_latest:
            # Get the latest prescription
            latest_prescription = Prescription_model.objects.filter(nurses=nurse, patient_id=patient_id).order_by('-date_of_prescription').first()
            if latest_prescription:
                patient_prescriptions.append({
                    'patient': PatientProfile.objects.get(id=patient_id),
                    'prescriptions': [latest_prescription]
                })
        elif show_previous:
            # Get all previous prescriptions except the latest one
            latest_prescription = Prescription_model.objects.filter(nurses=nurse, patient_id=patient_id).order_by('-date_of_prescription').first()
            previous_prescriptions = Prescription_model.objects.filter(nurses=nurse, patient_id=patient_id).exclude(id=latest_prescription.id)
            if previous_prescriptions:
                patient_prescriptions.append({
                    'patient': PatientProfile.objects.get(id=patient_id),
                    'prescriptions': previous_prescriptions.order_by('-date_of_prescription')
                })
        else:
            # Get the latest prescription by default
            latest_prescription = Prescription_model.objects.filter(nurses=nurse, patient_id=patient_id).order_by('-date_of_prescription').first()
            if latest_prescription:
                patient_prescriptions.append({
                    'patient': PatientProfile.objects.get(id=patient_id),
                    'prescriptions': [latest_prescription]
                })
    
    return render(request, 'nurse_temp/view_prescription_nurse.html', {'patient_prescriptions': patient_prescriptions})


from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Prescription_model

def view_past_prescriptions(request):
    if request.method == 'GET' and 'patient_id' in request.GET:
        patient_id = request.GET.get('patient_id')
        past_prescriptions = Prescription_model.objects.filter(patient_id=patient_id).order_by('-date_of_prescription')
        past_prescriptions_html = render_to_string('nurse_temp/past_prescriptions.html', {'past_prescriptions': past_prescriptions})
        return HttpResponse(past_prescriptions_html)
    else:
        # Handle case when patient_id is not provided or POST request is made
        return HttpResponse('Invalid request', status=400)


# approved appointments in nurse page

    
@login_required(login_url='login_page')
def nurse_approved_appointments(request):
    # Get the currently logged-in Nurse
    current_nurse = request.user

    # Filter approved appointments based on the logged-in Nurse's email
    approved_appointments = Appointment.objects.filter(is_approved=True, nurse__email=current_nurse.email)

    return render(request, 'nurse_temp/nurse_approved_appo.html', {'approved_appointments': approved_appointments})



# views.py for view_prescription_patient

from django.shortcuts import render, redirect
from .models import Nurse, PatientProfile, Prescription_model, Medicine
from django.contrib.auth.decorators import login_required

def patient_prescriptions(request, patient_id):
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    prescriptions = Prescription_model.objects.filter(patient=patient)
    return render(request, 'patient_prescriptions.html', {'patient': patient, 'patient_id':patient_id,'prescriptions': prescriptions})



#add member

def add_member(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        wardmem = request.POST.get('wardmem')
        
        phone = request.POST.get('phone')
        profile_photo = request.FILES.get('profile_photo')
        role = CustomUser.MEMBER
        print(role)

        # Check if a user with the same email and role exists
        if CustomUser.objects.filter(email=email, role=CustomUser.MEMBER).exists():
            messages.info(request, 'Email already exists')
            return redirect('add_member')

        # Check if a user with the same ward exists
        if Member.objects.filter(wardmem=wardmem).exists():
            messages.info(request, 'Ward already assigned to another Ashaworker')
            return redirect('add_member')

        # Create the user and Ashaworker records
        user = CustomUser.objects.create_user(email=email, password=password)
        user.role = CustomUser.MEMBER
        user.save()
        member = Member(user=user, Name=name, email=email, 
                         gender=gender, address=address, taluk=taluk, Panchayat=panchayat, wardmem=wardmem,
                         phone=phone, profile_photo=profile_photo)
        member.save()

        subject = 'Member Login Details'
        message = f'Registered as an Member. Your username: {email}, Password: {password}'
        from_email = settings.EMAIL_HOST_USER  # Your email address
        recipient_list = [user.email]  # Employee's email address

        send_mail(subject, message, from_email, recipient_list)

        return redirect('ad_member')
    else:
        return render(request, 'admin_temp/add_member.html')


#edit member
    
@login_required(login_url='login_page')
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        taluk = request.POST.get('taluk')
        panchayat = request.POST.get('panchayat')
        wardmem = request.POST.get('wardmem')
        
        phone = request.POST.get('phone')
        new_profile_photo = request.FILES.get('new_profile_photo')
        if new_profile_photo:
            member.profile_photo = new_profile_photo

        member.Name = name
        member.email = email
        member.set_password(password)
        
        member.gender = gender
        member.address = address
        member.taluk = taluk
        member.Panchayat = panchayat
        member.wardmem = wardmem
        
        member.phone = phone
        member.save()
        return redirect('ad_member')
    return render(request, 'admin_temp/edit_member.html', {'member': member})


# search members
@login_required(login_url='login_page')
def search_member(request):
    # Get the search query from the GET request
    search_query = request.GET.get('memname', '')

    # Filter Ashaworkers whose name contains the search query
    members = Member.objects.filter(Name__icontains=search_query, is_active=True)

    context = {
        'members': members,
        'search_query': search_query,
    }

    return render(request, 'admin_temp/ad_member.html', context)


# print member
@login_required(login_url='login_page')
def ad_member(request):
    # Retrieve the unique Panchayath values from the Ashaworker model
    unique_panchayaths = Member.objects.values_list('Panchayat', flat=True).distinct()

    # Retrieve the search parameter from the request
    search_query = request.GET.get('panchayath')

    # Retrieve all Ashaworkers if no search parameter is provided
    if not search_query:
        members = Member.objects.all()
    else:
        # Filter Ashaworkers based on the search parameter (panchayath)
        members = Member.objects.filter(Panchayat__icontains=search_query)

    return render(request, 'admin_temp/ad_member.html', {'members': members, 'unique_panchayaths': unique_panchayaths})





    

def check_wardmem_exists(request):
    wardmem = request.GET.get("wardmem", "")
    ward_exists = Member.objects.filter(wardmem=wardmem).exists()
    response_data = {"exists": ward_exists}
    return JsonResponse(response_data)



from django.contrib.auth.decorators import login_required
from .models import Member

@login_required
def patient_list_mem(request):
    # Retrieve the member associated with the logged-in user
    member = Member.objects.get(user=request.user)
    
    ward_filter = member.wardmem  # Assuming wardmem is the field containing the member's ward
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.none()  # Return an empty queryset
    
    # Assuming you want to display all available ward numbers for the member
    ward_numbers = PatientProfile.objects.filter(ward=ward_filter).values_list('ward', flat=True).distinct()
    
    return render(request, 'member_temp/patient_list_mem.html', {'patients': patients, 'ward_numbers': ward_numbers})

# ashaworkers list in member page
def asha_list_mem(request):
    # Retrieve the member associated with the logged-in user
    member_asha = Member.objects.get(user=request.user)
    
    ward_filter = member_asha.wardmem  # Assuming wardmem is the field containing the member's ward
    
    if ward_filter:
        asha = Ashaworker.objects.filter(ward=ward_filter)
    else:
        asha = PatientProfile.objects.none()  # Return an empty queryset
    
    # Assuming you want to display all available ward numbers for the member
    ward_numbers = PatientProfile.objects.filter(ward=ward_filter).values_list('ward', flat=True).distinct()
    
    return render(request, 'member_temp/ashaworker_Details.html', {'asha': asha, 'ward_numbers': ward_numbers})

#index page of member
def member_index(request):
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

    return render(request, 'member_temp/member_index.html', {
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
    future_appointments = Appointment.objects.filter(date__gt=current_date, status=True).order_by('date', 'slot__start_time')

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
        'future_appointments': future_appointments,
        
        
        
    })



@ashaworker_required
def asha_index(request):
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

    return render(request, 'asha_temp/asha_index.html', {
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
            elif user.role == CustomUser.MEMBER:
                login(request, user)
                return redirect('member_index')
            elif user.role == CustomUser.NURSE:
                login(request, user)
                return redirect('nurse_index')
            elif user.role == CustomUser.ADMIN:
                login(request, user)
                return redirect('admin_dashboard')
            elif user.role == CustomUser.MEMBER:
                login(request, user)
                return redirect('member_index')
            else:
                messages.info(request, "Invalid Role for Login")
        else:
            messages.info(request, "Invalid Login")
        return redirect('login_page')
    else:
        return render(request, 'login.html')    




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


def index(request):
    
    # Retrieve all Image objects
    images = Image.objects.all()

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve the CustomUser object for the authenticated user
        user = get_object_or_404(CustomUser, pk=request.user.id)
        print(user)
        user_pk = user.pk
        print(user_pk)

        # Retrieve the PatientProfile object for the authenticated user
        try:
            patient = PatientProfile.objects.get(user=user)
            print(patient)
        except PatientProfile.DoesNotExist:
            # Handle the case where the PatientProfile does not exist for the user
            patient = None
    else:
        user = None
        patient = None

    # Prepare the context for rendering the template
    context = {
        'images': images,
        'patient': patient,
        'user': user,
    }

    # Render the template with the context
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

# for ashaworker page
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
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
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
            first_name=first_name,
            last_name=last_name,
            doctor_notes=doctor_notes,
            medications_needed=medications_needed,
            treatments=treatments,
            current_conditions=current_conditions,
        )

        return redirect(reverse("ashaworker_view_medical_record", args=[patient_id]))

    return render(request, "medical_record.html", {"patient": patient,"medical_record": medical_record})

# for ashaworker page
def view_visit_history(request, patient_id):
    # Retrieve the patient based on the patient_id
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    # Retrieve the patient's medical records
    hv = home_visit.objects.filter(user=patient.user).order_by('-date')

    return render(request, "asha_temp/view_visit_history.html", {"patient": patient, "hv": hv})
# for admin page
def ad_view_home_visits(request, patient_id):
    # Retrieve the patient based on the patient_id
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    # Retrieve the patient's medical records
    hv = home_visit.objects.filter(user=patient.user).order_by('-date')

    return render(request, "admin_temp/ad_view_home_visits.html", {"patient": patient, "hv": hv})
# for admin page
def ad_home_visit(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.all()
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'admin_temp/ad_home_visit.html', {'patients': patients, 'ward_numbers': ward_numbers})


@login_required(login_url='login_page')
def admin_search_patient(request):
    # Get the search query from the GET request
    search_query = request.GET.get('patientname', '')

    # Filter Ashaworkers whose name contains the search query
    patients = PatientProfile.objects.filter(first_name__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'admin_temp/ad_home_visit.html', context)



# for ashaworker page
@login_required
def add_home_visit(request, patient_id):
    # Retrieve the patient based on the patient_id
    try:
        patient = PatientProfile.objects.get(pk=patient_id)
    except PatientProfile.DoesNotExist:
        return HttpResponse("Patient not found", status=404)

    if request.method == "POST":
        # Get the data from the form
        date = request.POST.get("date")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email= request.POST.get("email")
        start_time= request.POST.get("start_time")
        end_time= request.POST.get("end_time")

        
        home_visit.objects.create(
            user=patient.user,
            date=date,
            first_name=first_name,
            last_name=last_name,
            email=email,
            start_time=start_time,
            end_time=end_time,
            
        )

        return redirect(reverse("view_visit_history", args=[patient_id]))

    return render(request, "add_home_visit.html", {"patient": patient,"add_home_visit": add_home_visit})


# for ashaworker page
def Home_visit(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.all()
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'asha_temp/home_visit.html', {'patients': patients, 'ward_numbers': ward_numbers})






@login_required(login_url='login_page')
def asha_search_patient(request):
    # Get the search query from the GET request
    search_query = request.GET.get('patientname', '')

    # Filter Ashaworkers whose name contains the search query
    patients = PatientProfile.objects.filter(first_name__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'asha_temp/add_view_rec.html', context)



# for patient page
@login_required
def medical_record_search(request):
    if request.method == 'GET':
        selected_date = request.GET.get('selected_date')

        if selected_date:
            medical_record = MedicalRecord.objects.filter(user=request.user, date=selected_date).order_by('-date')
        else:
            medical_record = MedicalRecord.objects.filter(user=request.user).order_by('-date')

        return render(request, "medical_record_display.html", {"medical_record": medical_record})

# for patient page
@login_required
def medical_record_display(request):
    medical_record = MedicalRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, "medical_record_display.html", {"medical_record": medical_record})

def ashaworker_view_medical_record(request, patient_id):
    # Retrieve the patient based on the patient_id
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    # Retrieve the patient's medical records
    medical_record = MedicalRecord.objects.filter(user=patient.user).order_by('-date')

    return render(request, "asha_temp/asha_med_rec.html", {"patient": patient, "medical_record": medical_record})


from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_medical_record_pdf(request):
    # Assuming you have imported MedicalRecord model and defined the user's relationship
    medical_records = MedicalRecord.objects.filter(user=request.user).order_by('-date')
    patient_profile = request.user.patientprofile  # Assuming you have a one-to-one relationship
    first_name = patient_profile.first_name
    last_name = patient_profile.last_name

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, title="Medical Record")
    styles = getSampleStyleSheet()

    elements = []

    main_heading_text = "<center><b>Gentle Haloes Palliative Care</b></center>"
    main_heading = Paragraph(main_heading_text, styles['Heading1'])
    elements.append(main_heading)
    elements.append(Spacer(1, 10))

    sub_heading_text = "<center><b>Parathodu Grama Panchayath</b></center>"
    sub_heading = Paragraph(sub_heading_text, styles['Heading2'])
    elements.append(sub_heading)

    sub_heading_medical_record = "<center><b>Medical Record</b></center>"
    sub_heading_medical = Paragraph(sub_heading_medical_record, styles['Heading2'])
    elements.append(sub_heading_medical)

    patient_name_text = "<b>Patient Name:</b> {} {}".format(first_name, last_name)
    patient_name = Paragraph(patient_name_text, styles['Normal'])
    elements.append(patient_name)
    elements.append(Spacer(1, 20))

    for record in medical_records:
        elements.append(Paragraph("<b>Date:</b> {}".format(record.date), styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Doctor's Notes:</b> {}".format(record.doctor_notes), styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Medications Needed:</b> {}".format(record.medications_needed), styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Treatments:</b> {}".format(record.treatments), styles['Normal']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Current Conditions:</b> {}".format(record.current_conditions), styles['Normal']))
        elements.append(Spacer(1, 10))

    pdf.build(elements)
    buffer.seek(0)

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


def appointment_chart_asha(request):
    # Query the database to count the number of appointments for each patient
    appointments_count = Appointment.objects.values('user__email').annotate(appointment_count=Count('id'))

    # Extract the patient usernames and appointment counts for the chart
    patient_usernames = [appointment['user__email'] for appointment in appointments_count]
    appointment_counts = [appointment['appointment_count'] for appointment in appointments_count]

    return render(request, 'asha_temp/appointment_chart_asha.html', {'patient_usernames': patient_usernames, 'appointment_counts': appointment_counts})




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

def hca_index(request):
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

    return render(request, 'hca_temp/hca_index.html', {
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

@login_required(login_url='login_page')
def hca_patient_users(request):
    # patients = CustomUser.objects.filter(role=CustomUser.PATIENTS)
    patients = PatientProfile.objects.filter(is_active=True)
    return render(request, 'hca_temp/hca_patient_users.html', {'patients': patients})


@login_required(login_url='login_page')
def hca_patients_by_ward(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.filter(is_active=True)
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'hca_temp/hca_patients_by_ward.html', {'patients': patients, 'ward_numbers': ward_numbers})


@login_required(login_url='login_page')
def hca_add_view_rec(request):
    ward_filter = request.GET.get('ward')
    
    if ward_filter:
        patients = PatientProfile.objects.filter(ward=ward_filter)
    else:
        patients = PatientProfile.objects.filter(is_active=True)
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'hca_temp/hca_add_view_rec.html', {'patients': patients, 'ward_numbers': ward_numbers})

def hca_view_medical_record(request, patient_id):
    # Retrieve the patient based on the patient_id
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    # Retrieve the patient's medical records
    medical_record = MedicalRecord.objects.filter(user=patient.user).order_by('-date')

    return render(request, "hca_temp/hca_med_rec.html", {"patient": patient, "medical_record": medical_record})

@login_required(login_url='login_page')
def hca_search_patient(request):
    # Get the search query from the GET request
    search_query = request.GET.get('patientname', '')

    # Filter Ashaworkers whose name contains the search query
    patients = PatientProfile.objects.filter(first_name__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'hca_temp/hca_patients_by_ward.html', context)

@login_required(login_url='login_page')
def hca_med_search_patient(request):
    # Get the search query from the GET request
    search_query = request.GET.get('patientname', '')

    # Filter Ashaworkers whose name contains the search query
    patients = PatientProfile.objects.filter(first_name__icontains=search_query)
    # patients = PatientProfile.objects.filter(last_name__icontains=search_query)
    

    context = {
        'patients': patients,
        'search_query': search_query,
    }

    return render(request, 'hca_temp/hca_add_view_rec.html', context)


@login_required(login_url='login_page')
def edit_hca_pro(request):
    user = request.user
    hca = get_object_or_404(Hca, user=user)

    if request.method == "POST":
        # Process the form data and save/update the profile
        hca.hcaname = request.POST.get('hcaname')
        hca.email = request.POST.get('email')
        hca.address = request.POST.get('address')
        hca.postal = request.POST.get('postal')
        hca.phone = request.POST.get('phone')
        hca.panchayat = request.POST.get('panchayat')
        hca.taluk = request.POST.get('taluk')
        # hca.year_hca = request.POST.get('year_hca')
        new_li_photo = request.FILES.get('new_li_photo')
        if new_li_photo:
            # Delete the old license certificate if it exists
            if hca.license_certificate:
                fs = FileSystemStorage()
                fs.delete(hca.license_certificate.name)

            # Save the new license certificate to a specific directory
            fs = FileSystemStorage()
            filename = fs.save(f"lic_cert/{new_li_photo.name}", new_li_photo)
            hca.license_certificate = filename
        new_profile_photo = request.FILES.get('new_profile_photo')
        if new_profile_photo:
            # Delete the old profile photo if it exists
            if hca.profile_photo:
                fs = FileSystemStorage()
                fs.delete(hca.profile_photo.name)

            # Save the new profile photo to a specific directory
            fs = FileSystemStorage()
            filename = fs.save(f"profile_photos/{new_profile_photo.name}", new_profile_photo)
            hca.profile_photo = filename 
        hca.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('pro_hca')  # Redirect to the profile page
    
    context = {
        'user': user,
        'hca': hca
    }

    return render(request, 'hca_temp/edit_hca_pro.html', context)

@login_required(login_url='login_page')
def pro_hca(request):
    hca = Hca.objects.filter(user=request.user).first() 
    return render(request, 'hca_temp/pro_hca.html', {'hca': hca})

def appointment_view(request):
    # Get the user's appointments excluding canceled ones
    user_appointments = Appointment.objects.filter(user=request.user, status=True)

    return render(request, 'appointment_view.html', {'appointments': user_appointments})


from django.http import JsonResponse
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        # Check if the appointment is approved
        if appointment.is_approved:
            return JsonResponse({'message': 'Cannot cancel an approved appointment'}, status=400)
        
        # Update the status to canceled
        appointment.status = False
        appointment.save()
        
        return JsonResponse({'message': 'Appointment canceled successfully', 'appointment_id': appointment_id})
    except Appointment.DoesNotExist:
        return JsonResponse({'message': 'Appointment not found'}, status=404)



from django.http import JsonResponse

def check_approval_status(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.is_approved:
            return JsonResponse({'approved': True})
        else:
            return JsonResponse({'approved': False})
    except Appointment.DoesNotExist:
        return JsonResponse({'message': 'Appointment not found'}, status=404)
    

# Medicine Section
    
def add_medicine_category(request):
     if request.method == 'POST':
         category_name = request.POST['category_name']  # Get the form field values
         description  = request.POST['description']

         ob = MedicineCategory()
         ob.category_name = category_name
         ob.description = description 
         ob.save()
                
                 # Redirect to the view_medicine_category page after successful save
         return redirect('view_medicine_category')
        
    
     # Render the form page for GET requests
     return render(request, 'admin_temp/add_medicine_category.html')

def view_medicine_category(request):
    categories = MedicineCategory.objects.filter(is_active=True)
    return render(request, 'admin_temp/view_medicine_category.html', {'categories': categories})



from django.shortcuts import get_object_or_404, redirect

def edit_medicine_category(request, pk):
    category = get_object_or_404(MedicineCategory, pk=pk)
    if request.method == 'POST':
        category.category_name = request.POST['category_name']
        category.description = request.POST['description']
        category.save()
        return redirect('view_medicine_category')
    return render(request, 'admin_temp/edit_medicine_category.html', {'category': category})



def delete_medicine_category(request, medcatid):
    ob = get_object_or_404(MedicineCategory, MedCatId=medcatid)  # Replace 'MedicineCategory' with your actual model name

    if request.method == 'POST':
        # Delete the medicine category object
        ob.is_active=False
        ob.save()
        # request.session['delete_category'] = True
        return redirect('view_medicine_category')

    return render(request, 'admin_temp/delete_medicine_category.html', {'ob': ob})


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse
from .models import MedicineCategory

def generate_category_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medicine_category_details.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Get sample style sheet
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading1"]
    subheading_style = ParagraphStyle(name='SubHeading', parent=styles["Normal"])
    subheading_style.fontSize = 16
    subheading_style.textColor = colors.blue
    subheading_style.spaceAfter = 10
    subheading_style.alignment = 1 
    heading_style.alignment = 1 

    main_heading = Paragraph("<center>Gentle Haloes Palliative Care Services</center>", heading_style)
    content = [main_heading]

    # Add subheading
    sub_heading = Paragraph("<center>Medicine Category Details</center>", subheading_style)
    content.append(sub_heading)
    content.append(Spacer(1, 20))
    

    # Get medicine categories
    categories = MedicineCategory.objects.filter(is_active=True)
    for index, category in enumerate(categories, start=1):
        content.append(Paragraph(f"<b>Medicine {index}</b>", normal_style))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"<b>Category Name:</b> {category.category_name}", normal_style))
        content.append(Paragraph(f"<b>Description:</b> {category.description}", normal_style))
        content.append(Paragraph("<u>--------------------------------------------------------</u>", normal_style))  # Separator between categories
        content.append(Spacer(1, 10)) 
    # Add content to the PDF document
    doc.build(content)

    return response


def add_medicine(request):
    if request.method == 'POST':
        # Get data from the form
        medicine_name = request.POST['medicineName']
        details = request.POST['details']
        company_name = request.POST['companyName']
        expiryDate = request.POST['expiryDate']
        contains = request.POST['contains']
        dosage = request.POST['dosage']
        price = request.POST['price']
        category_id = request.POST['category']

        # Get the MedicineCategory instance based on the selected category_id
        category = get_object_or_404(MedicineCategory, pk=category_id)

        # Create and save a Medicine object to the database with the category instance
        medicine = Medicine(
            medicineName=medicine_name,
            details=details,
            companyName=company_name,
            expiryDate=expiryDate,
            contains=contains,
            dosage=dosage,
            price=price,
            MedCatId=category,
        )
        medicine.save()

        return redirect('view_medicine')  # Redirect to a success page or another URL
    medcat = MedicineCategory.objects.all()
    print(medcat)
    context = {'medcat': medcat}
    return render(request, 'admin_temp/add_medicine.html', context)

def view_medicine(request):
    med = Medicine.objects.all()
    print(med)
    return render(request,'admin_temp/view_medicine.html',{'med': med})

from django.shortcuts import render, get_object_or_404

def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)

    if request.method == 'POST':
        # Update medicine details
        medicine.medicineName = request.POST['medicineName']
        medicine.details = request.POST['details']
        medicine.companyName = request.POST['companyName']
        medicine.expiryDate = request.POST['expiryDate']
        medicine.contains = request.POST['contains']
        medicine.dosage = request.POST['dosage']
        medicine.price = request.POST['price']
        medicine.MedCatId = MedicineCategory.objects.get(pk=request.POST['category'])
        medicine.save()

        return redirect('view_medicine')  # Redirect to view medicine page

    medcat = MedicineCategory.objects.all()
    context = {'medicine': medicine, 'medcat': medcat}
    return render(request, 'admin_temp/edit_medicine.html', context)


from django.shortcuts import redirect, get_object_or_404

def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    medicine.delete()
    return redirect('view_medicine')  # Redirect to view medicine page after deletion





from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.http import HttpResponse

def med_generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medicine_details.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Get sample style sheet
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading1"]
    subheading_style = ParagraphStyle(name='SubHeading', parent=styles["Normal"])
    subheading_style.fontSize = 16
    subheading_style.textColor = colors.blue
    subheading_style.spaceAfter = 10
    subheading_style.alignment = 1 
    heading_style.alignment = 1 

    main_heading = Paragraph("<center>Gentle Haloes Palliative Care Services</center>", heading_style)
    content = [main_heading]

    # Add subheading
    sub_heading = Paragraph("<center>Medicine Details</center>", subheading_style)
    content.append(sub_heading)
    content.append(Spacer(1, 20))
    

    # Add medicine details to the document
    medicines = Medicine.objects.all()
    for medicine in medicines:
        content.append(Paragraph(f"<b>Medicine Name:</b> {medicine.medicineName}", normal_style))
        content.append(Paragraph(f"<b>Details:</b> {medicine.details}", normal_style))
        content.append(Paragraph(f"<b>Company:</b> {medicine.companyName}", normal_style))
        content.append(Paragraph(f"<b>Expiry Date:</b> {medicine.expiryDate}", normal_style))
        content.append(Paragraph(f"<b>Contains:</b> {medicine.contains}", normal_style))
        content.append(Paragraph(f"<b>Dosage:</b> {medicine.dosage}", normal_style))
        content.append(Paragraph(f"<b>Price:</b> {medicine.price}", normal_style))
        content.append(Paragraph(f"<b>Category:</b> {medicine.MedCatId.category_name}", normal_style))
        content.append(Paragraph("<u>--------------------------------------------------------</u>", normal_style))  # Separator between medicines
        content.append(Spacer(1, 10))  
    # Add content to the PDF document
    doc.build(content)

    return response


# Apply Leave 
from django.shortcuts import render
from django.http import HttpResponseNotAllowed
def apply_leave(request):
    if request.method == 'GET':
        # If it's a GET request, render the template for applying leave
        return render(request, 'apply_leave.html')  # Replace 'apply_leave.html' with the actual template name

    elif request.method == 'POST':
        # Your existing POST request handling code
        user = request.user
        
        # Determine the staff member type and retrieve the corresponding staff instance
        try:
            staff_member = Nurse.objects.get(user=user)
        except Nurse.DoesNotExist:
            try:
                staff_member = Ashaworker.objects.get(user=user)
            except Ashaworker.DoesNotExist:
                staff_member = Member.objects.get(user=user)
        
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        # Create a new leave instance
        leave = Leave.objects.create(
            nurse_member=staff_member if isinstance(staff_member, Nurse) else None,
            asha_member=staff_member if isinstance(staff_member, Ashaworker) else None,
            mem_member=staff_member if isinstance(staff_member, Member) else None,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return redirect('apply_leave')

    else:
        # Handle other request methods if necessary
        return HttpResponseNotAllowed(['GET', 'POST'])

def view_leave(request):
    user = request.user
    staff_member = None
    
    # Determine the staff member type and retrieve the corresponding staff instance
    try:
        staff_member = Nurse.objects.get(user=user)
    except Nurse.DoesNotExist:
        try:
            staff_member = Ashaworker.objects.get(user=user)
        except Ashaworker.DoesNotExist:
            staff_member = Member.objects.get(user=user)
    
    if staff_member:
        if isinstance(staff_member, Nurse):
            leaves = Leave.objects.filter(nurse_member=staff_member)
        elif isinstance(staff_member, Ashaworker):
            leaves = Leave.objects.filter(asha_member=staff_member)
        elif isinstance(staff_member, Member):
            leaves = Leave.objects.filter(me1m_member=staff_member)
    else:
        leaves = []

    return render(request, 'view_leave.html', {'leaves': leaves})

# leave list in admin panel

def leave_list(request):
    # Retrieve all leave entries for doctors, receptionists, and pharmacists
    nurse_leaves = Leave.objects.filter(nurse_member__isnull=False)
    asha_leaves = Leave.objects.filter(asha_member__isnull=False)
    mem_leaves = Leave.objects.filter(mem_member__isnull=False)
    
    context = {
        'nurse_leaves': nurse_leaves,
        'asha_leaves': asha_leaves,
        'mem_leaves': mem_leaves
    }
    
    return render(request, 'admin_temp/leave_list.html', context)

from django.http import JsonResponse

def approve_leave(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        leave = Leave.objects.get(id=leave_id)
        leave.status = 'Approved'
        leave.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def reject_leave(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        leave = Leave.objects.get(id=leave_id)
        leave.status = 'Rejected'
        leave.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# meical record section in nurse page

@login_required
def nurse_medical_record(request, patient_id):
    
    try:
        patient = PatientProfile.objects.get(pk=patient_id)
    except PatientProfile.DoesNotExist:
        return HttpResponse("Patient not found", status=404)

    if request.method == "POST":
        # Get the data from the form
        date = request.POST.get("date")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        doctor_notes = request.POST.get("doctor_notes")
        medications_needed = request.POST.get("medications_needed")
        treatments = request.POST.get("treatments")
        current_conditions = request.POST.get("current_conditions")

        
        MedicalRecord.objects.create(
            user=patient.user,
            date=date,
            first_name=first_name,
            last_name=last_name,
            doctor_notes=doctor_notes,
            medications_needed=medications_needed,
            treatments=treatments,
            current_conditions=current_conditions,
        )

        return redirect(reverse("nurse_view_medical_record", args=[patient_id]))

    return render(request, "nurse_temp/medical_record_nurse.html", {"patient": patient,"medical_record": medical_record})

def nurse_view_medical_record(request, patient_id):
    # Retrieve the patient based on the patient_id
    patient = get_object_or_404(PatientProfile, pk=patient_id)

    # Retrieve the patient's medical records
    medical_record = MedicalRecord.objects.filter(user=patient.user).order_by('-date')

    return render(request, "nurse_temp/nurse_med_rec.html", {"patient": patient, "medical_record": medical_record})

def add_view_rec_nurse(request):
   
    nurse = Nurse.objects.get(user=request.user)
    ward = nurse.wardnurse
    
    patients = PatientProfile.objects.filter(ward=ward, is_active=True)
    
    ward_numbers = PatientProfile.objects.values_list('ward', flat=True).distinct()
    
    return render(request, 'nurse_temp/add_view_rec_nurse.html', {'patients': patients, 'ward_numbers': ward_numbers})

