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
from GHapp.views import login_page,edit_gallery_images, appointment_form,register,ad_gallery,loggout,add_asha,ResetPasswordView,ChangePasswordView
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

   
    
    path('index-2', views.index2, name="index-2"), 
    
  
    path('edit_patient_profile', views.edit_patient_profile, name='edit_patient_profile'),
    path('print_patient_profile', views.print_patient_profile, name='print_patient_profile'),
    
     path('edit_asha_pro', views.edit_asha_pro, name='edit_asha_pro'),
     path('pro_ashaworker', views.pro_ashaworker, name="pro_ashaworker"),



    path('ad_ashaworker', views.ad_ashaworker, name="ad_ashaworker"),
   


    path('check-ward-exists/', views.check_ward_exists, name='check_ward_exists'),
    path('add_asha', add_asha, name="add_asha"),  # Add this line for adding Asha Worker
    path('patients', views.patients, name="patients"),
    # path('schedule', views.schedule, name="schedule"),
    path('schedule/', views.schedule, name='schedule'),
    

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

    path('ad_hca', views.ad_hca, name="ad_hca"),
    path('add_hca', views.add_hca, name="add_hca"),
    path('edit_hca/<int:hca_id>/', views.edit_hca, name='edit_hca'),

    path('hca_index', views.hca_index, name="hca_index"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
