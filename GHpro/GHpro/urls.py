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
from GHapp.views import admin_login,login_page,hca_signup, register,ad_gallery,loggout,add_asha,appointment_form,ResetPasswordView,ChangePasswordView
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
    path('doctor', views.doctor, name="doctor"),
    path('testimonial', views.testimonial, name="testimonial"),
    path('contact', views.contact, name="contact"),
    
    path('index-2', views.index2, name="index-2"), 
    
    # path('patient_profile', views.patient_profile, name="patient_profile"),
    # path('edit_patient_profile', views.edit_patient_profile, name="edit_patient_profile"),
    
    path('patient_profile', views.patient_profile, name='patient_profile'),

    # path('edit_patient_profile',views.edit_patient_profile, name='edit_patient_profile'),
    



    path('ad_ashaworker', views.ad_ashaworker, name="ad_ashaworker"),
    path('add_asha', add_asha, name="add_asha"),  # Add this line for adding Asha Worker
    path('patients', views.patients, name="patients"),
    path('schedule', views.schedule, name="schedule"),
    path('add-patient', views.addpatient, name="add-patient"),
    # path('edit_asha', edit_asha, name="edit_asha"),

    path('appointments', views.ad_appointment, name="appointments"), 
    # path('patient_profile', views.user_details_appointment, name="patient_profile"), 

    path('adgallery', ad_gallery, name="adgallery"), 
    path('admin_login', admin_login, name='admin_login'),
    # path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'), 

    # path('asha_dashboard', views.asha_dashboard, name='asha_dashboard'),



    path('login_page', login_page, name='login_page'),
    path('register', register, name='register'),
    path('hca_signup', hca_signup, name='hca_signup'),
    path('loggout', loggout, name='loggout'),  

    path('edit_gallery', views.edit_gallery, name="edit_gallery"),
    path('edit_asha/<int:asha_id>/', views.edit_asha, name='edit_asha'),
    path('delete_asha/<int:asha_id>/', views.delete_asha, name='delete_asha'),
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
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
