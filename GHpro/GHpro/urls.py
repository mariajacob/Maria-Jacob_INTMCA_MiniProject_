"""
URL configuration for GHpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from GHapp import views
from django.contrib import admin
from django.urls import path, include
from GHapp.views import login_page,edit_gallery_images, patient_prescriptions,appointment_form,register,ad_gallery,loggout,add_asha,add_member,ResetPasswordView,ChangePasswordView
from GHapp.views import login_page,edit_gallery_images, add_nurse,add_member,appointment_form,register,ad_gallery,loggout,add_asha,ResetPasswordView,ChangePasswordView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("allauth.urls")), 

    path('', views.index, name="index"),
    path('appointment_form', appointment_form, name="appointment_form"),
    path('about', views.about, name="about"),
    path('treatment', views.treatment, name="treatment"),
    path('gallery', views.gallery, name="gallery"),

    path('resources', views.resources, name="resources"),
    path('resources_details/<int:blog_id>/', views.resources_details, name="resources_details"),
     path('search-resources/', views.search_resources, name='search_resources'),

    path('testimonial', views.testimonial, name="testimonial"),
    path('contact', views.contact, name="contact"),
    path('donation', views.donation, name="donation"),


    path('blog', views.blog, name="blog"),
    # path('blog-details', views.blog_details, name="blog-details"),
    path('blog_details/<int:blog_id>/', views.blog_details, name='blog-details'),
    path('add-blog', views.add_blog, name="add-blog"),
   
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    

    
    # path('medical_record', views.medical_record, name="medical_record"),
    path('medical_record/<int:patient_id>/', views.medical_record, name='medical_record'),

    # path('medical_record/', views.medical_record, name='medical_record'),
    path('medical_record_display', views.medical_record_display, name="medical_record_display"),
    path('medical_record_search/', views.medical_record_search, name='medical_record_search'),

    path('ashaworker/medical_record/<int:patient_id>/', views.ashaworker_view_medical_record, name='ashaworker_view_medical_record'),
    path('asha_search_patient/', views.asha_search_patient, name='asha_search_patient'),
    
    path('Home_visit/', views.Home_visit, name='Home_visit'),
    path('add_home_visit/<int:patient_id>/', views.add_home_visit, name='add_home_visit'),
    path('ashaworker/add_home_visit/<int:patient_id>/', views.view_visit_history, name='view_visit_history'),
    path('ad_home_visit/', views.ad_home_visit, name='ad_home_visit'),
    path('ashaworker/ad_view_home_visits/<int:patient_id>/', views.ad_view_home_visits, name='ad_view_home_visits'),
  
    path('admin_search_patient/', views.admin_search_patient, name='admin_search_patient'),
  
    path('edit_patient_profile', views.edit_patient_profile, name='edit_patient_profile'),
    path('print_patient_profile', views.print_patient_profile, name='print_patient_profile'),
    
     path('edit_asha_pro', views.edit_asha_pro, name='edit_asha_pro'),
     path('pro_ashaworker', views.pro_ashaworker, name="pro_ashaworker"),

#add panchayath and ward
    path('ad_panward', views.ad_panward, name="ad_panward"),
    path('add_panward', views.add_panward, name="add_panward"),
    path('get_wards/', views.get_wards, name='get_wards'),
    # path('get_wards_mem/', views.get_wards_mem, name='get_wards_mem'),

    path('ad_ashaworker', views.ad_ashaworker, name="ad_ashaworker"),
   

    path('get_times/', views.get_times, name='get_times'),
    path('check-ward-exists/', views.check_ward_exists, name='check_ward_exists'),
    path('add_asha', add_asha, name="add_asha"),  # Add this line for adding Asha Worker

# Add this line for adding Member
    path('ad_member', views.ad_member, name="ad_member"),
    path('add_member', add_member, name="add_member"),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('check-wardmem-exists/', views.check_wardmem_exists, name='check_wardmem_exists'),
    path('patient_list_mem/', views.patient_list_mem, name='patient_list_mem'),

    #index page of member
    path('member_index', views.member_index, name="member_index"),


    # Nurse Section
    path('nurse_index', views.nurse_index, name="nurse_index"),
    path('ad_nurse', views.ad_nurse, name="ad_nurse"),
    path('add_nurse', add_nurse, name="add_nurse"),
    # path('add_prescription', views.add_prescription, name="add_prescription"),
    path('add_prescription/', views.add_prescription, name='add_prescription'),
    path('view_past_prescriptions', views.view_past_prescriptions, name='view_past_prescriptions'),
    # view prescrption nurse
    path('view_prescription_nurse/', views.view_prescription_nurse, name='view_prescription_nurse'),
    path('nurse_approved_appo', views.nurse_approved_appointments, name='nurse_approved_appo'),


    path('patient_list_nurse', views.patient_list_nurse, name="patient_list_nurse"),


 # view prescrption paatients
     path('patient_prescriptions/<int:patient_id>/', views.patient_prescriptions, name='patient_prescriptions'),




    

    # Add this line for adding Member
    path('ad_member', views.ad_member, name="ad_member"),
    path('add_member', add_member, name="add_member"),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('check-wardmem-exists/', views.check_wardmem_exists, name='check_wardmem_exists'),
    path('patient_list_mem/', views.patient_list_mem, name='patient_list_mem'),
    path('asha_list_mem/', views.asha_list_mem, name='asha_list_mem'),
    

    # search member
    path('search-member/', views.search_member, name='search_member'),
    #index page of member
    path('member_index', views.member_index, name="member_index"),

    path('patients', views.patients, name="patients"),

    path('delete_patients/<int:patient_id>/', views.delete_patients, name='delete_patients'),

    # path('schedule', views.schedule, name="schedule"),
    path('schedule/', views.schedule, name='schedule'),
    

    # path('get_times/', views.get_times, name='get_times'),

     path('get_dates_for_ashaworker/', views.get_dates_for_ashaworker, name='get_dates_for_ashaworker'),

    # URL for getting time slots based on selected Ashaworker and date
    path('get_timeslots_for_date/', views.get_timeslots_for_date, name='get_timeslots_for_date'),

    # path('get_ashaworker_schedule/', views.get_ashaworker_schedule, name='get_ashaworker_schedule'),
    # path('ashaworker_schedules/<int:ashaworker_id>/', views.ashaworker_schedules, name='ashaworker_schedules'),



     path('asha_timeslots_shows', views.asha_timeslots_shows, name="asha_timeslots_shows"),
     path('asha_timeslots', views.asha_timeslots, name="asha_timeslots"),
    
    
    
    
    # path('add-patient', views.addpatient, name="add-patient"),
    

    path('appointments', views.ad_appointment, name="appointments"),
    path('current_appointment', views.current_appointment, name="current_appointment"),
    path('future_appointment', views.future_appointment, name="future_appointment"),
    path('past_appointment', views.past_appointment, name="past_appointment"), 
    
   

    path('adgallery', ad_gallery, name="adgallery"), 
   
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'), 
    path('search-ashaworker/', views.search_ashaworker, name='search_ashaworker'),

    

    path('asha_index', views.asha_index, name='asha_index'), 
    
    

    
    path('asha_approved_appo', views.asha_approved_appointments, name='asha_approved_appo'),
    path('approve-appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    # path('pending-appointment/<int:appointment_id>/', views.pending_appointment, name='pending_appointment'),
    
    path('patient_users/', views.patient_users, name='patient_users'),
    path('patients_by_ward/', views.patients_by_ward, name='patients_by_ward'),
    path('add_view_rec/', views.add_view_rec, name='add_view_rec'),

    path('search-patient/', views.search_patient, name='search_patient'),
   

    path('login_page', login_page, name='login_page'),
    path('register', register, name='register'),
   
    path('loggout', loggout, name='loggout'),  

    # path('edit_gallery', views.edit_gallery, name="edit_gallery"),
    path('dis_gallery', views.dis_gallery, name='dis_gallery'),
    path('edit_gallery_images/<int:image_id>/', edit_gallery_images, name='edit_gallery_images'),
    path('soft_delete_image/<int:image_id>/', views.soft_delete_image, name='soft_delete_image'),
    
    path('delete_asha/<int:asha_id>/', views.delete_asha, name='delete_asha'),

    path('edit_asha/<int:asha_id>/', views.edit_asha, name='edit_asha'),
 

    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registraion/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registraion/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),








    path('payment/<int:donat_id>/', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

    path('generate_pdf/', views.generate_medical_record_pdf, name='generate_medical_record_pdf'),
    

    path('appointment_chart/', views.appointment_chart, name='appointment_chart'),
    path('ashaworker_appointment_chart/', views.ashaworker_appointment_chart, name='ashaworker_appointment_chart'),

    path('appointment_chart_asha/', views.appointment_chart_asha, name='appointment_chart_asha'),

    path('ad_hca', views.ad_hca, name="ad_hca"),
    path('add_hca', views.add_hca, name="add_hca"),
    path('edit_hca/<int:hca_id>/', views.edit_hca, name='edit_hca'),

    path('hca_index', views.hca_index, name="hca_index"),
    path('hca_patient_users/', views.hca_patient_users, name='hca_patient_users'),
    path('hca_patients_by_ward/', views.hca_patients_by_ward, name='hca_patients_by_ward'),
    path('hca_add_view_rec/', views.hca_add_view_rec, name='hca_add_view_rec'),
    path('hca_search_patient/', views.hca_search_patient, name='hca_search_patient'),
    path('hca_med_search_patient/', views.hca_med_search_patient, name='hca_med_search_patient'),
    path('hca/medical_record/<int:patient_id>/', views.hca_view_medical_record, name='hca_view_medical_record'),
    path('edit_hca_pro', views.edit_hca_pro, name='edit_hca_pro'),
    path('pro_hca', views.pro_hca, name='pro_hca'),

    path('appointment_view/', views.appointment_view, name='appointment_view'),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('check_approval_status/<int:appointment_id>/', views.check_approval_status, name='check_approval_status'),

# Medicine Section
    path('add_medicine_category', views.add_medicine_category, name="add_medicine_category"),
    path('view_medicine_category', views.view_medicine_category, name="view_medicine_category"),
    path('edit_medicine_category/<int:pk>/', views.edit_medicine_category, name='edit_medicine_category'),
    path('delete_medicine_category/<int:medcatid>/',views.delete_medicine_category,name='delete_medicine_category'),
    path('generate_category_pdf/', views.generate_category_pdf, name='generate_category_pdf'),
    path('add_medicine', views.add_medicine, name="add_medicine"),
    path('view_medicine', views.view_medicine, name="view_medicine"),
    path('edit_medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('delete_medicine/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('med_generate_pdf/', views.med_generate_pdf, name='med_generate_pdf'),
    
    # Apply Leave
    path('apply_leave', views.apply_leave, name="apply_leave"),
    path('view_leave', views.view_leave, name="view_leave"),
    path('leave_list', views.leave_list, name="leave_list"), 
    path('approve-leave/', views.approve_leave, name='approve_leave'),
    path('reject-leave/', views.reject_leave, name='reject_leave'),
    # path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    # path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    # medical record in nurse

    
    path('nurse_medical_record/<int:patient_id>/', views.nurse_medical_record, name='nurse_medical_record'),
    path('nurse_view_medical_record/<int:patient_id>/', views.nurse_view_medical_record, name='nurse_view_medical_record'),
    path('add_view_rec_nurse/', views.add_view_rec_nurse, name='add_view_rec_nurse'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
