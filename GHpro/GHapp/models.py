from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
   
    def create_user(self, email, password=None, role=None):
        if not email:
         raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role,  # Set the role here
    )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role=4
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    PATIENTS = 1
    ASHAWORKER = 2
    HCA = 3
    ADMIN = 4

    ROLE_CHOICE = (
        ( PATIENTS, ' PATIENTS'),
        (ASHAWORKER, 'ASHAWORKER'),
        (HCA, 'HCA'),
        (ADMIN,'ADMIN'),
    
    )

    username=None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    REQUIRED_FIELDS = []

    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class Ashaworker(models.Model):
     
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    Name = models.CharField(max_length=100)
    
    email = models.EmailField(blank=True, null=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, password):
        # Hash and set the password
        self.admin_set_password = make_password(password)
    date_of_birth = models.CharField(max_length=100)
    date_of_join = models.CharField(max_length=100)
    
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    taluk = models.CharField(max_length=100)
    Panchayat = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    
    postal = models.IntegerField()
    phone = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    edu_level=models.CharField(max_length=100,choices=[('High School', 'High School'), ('Bachelors Degree', 'Bachelors Degree'), ('Masters Degree', 'Masters Degree')],blank=True, null=True)
    edu_inst=models.CharField(max_length=100,blank=True, null=True)
    year_pass_edu=models.IntegerField(blank=True, null=True)
    edu_certificate=models.FileField(upload_to='edu_cert/', blank=True, null=True)
    add_training=models.CharField(max_length=100,blank=True, null=True)
    add_training_inst=models.CharField(max_length=100,blank=True, null=True)
    year_pass_add=models.IntegerField(blank=True, null=True)
    add_certificate=models.FileField(upload_to='add_cert/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    
    class Meta:
            unique_together = (("id", "ward"),)
    # pin = models.IntegerField()
    # bio=models.TextField()

    def _str_(self):
        return self.Name








    
class Image(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')  # 'gallery/' is the directory where images will be stored

    def __str__(self):
        return self.title
    


class PatientProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    birth_date = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    house_name = models.CharField(max_length=100, null=True,blank=True)
    house_no = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    ward = models.CharField(max_length=100)
    pin_code = models.IntegerField(null=True,blank=True)
    phone_number = models.IntegerField(null=True,blank=True)
    
    current_diagnosis = models.CharField(max_length=100, null=True,blank=True)
    past_med_condition = models.CharField(max_length=100, null=True,blank=True)
    surgical_history = models.CharField(max_length=100, null=True,blank=True)
    
    allergies = models.CharField(max_length=100, null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    bmi = models.IntegerField(null=True,blank=True)
    medication_names = models.CharField(max_length=100, null=True,blank=True)
    dosage = models.CharField(max_length=12,null=True,blank=True)
    frequency = models.CharField(max_length=12,null=True,blank=True)
    
    def _str_(self):
        return self.first_name

class Appointment(models.Model):
   
    is_approved=models.BooleanField(default=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    # date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField(null=True,blank=True)
    ward_asha = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    # id_proof = models.FileField(upload_to='id_proofs/',null=True,blank=True)
    medical_conditions = models.TextField(null=True,blank=True)
    urgency = models.CharField(max_length=50, choices=[('Routine check-up', 'Routine check-up'), ('Non-urgent medical check-up', 'Non-urgent medical check-up'), ('Urgent medical check-up', 'Urgent medical check-up')],null=True,blank=True)
    medication_names = models.TextField(null=True,blank=True)
    symptoms = models.TextField(null=True,blank=True)
    preferred_date = models.DateField(null=True,blank=True)
    preferred_time = models.CharField(max_length=20, choices=[('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), ('01:00 PM', '01:00 PM')],null=True,blank=True)

    def __str__(self):
        return self.email

class MedicalRecord(models.Model):
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    doctor_notes = models.TextField()
    medications_needed = models.TextField()
    treatments = models.TextField()
    current_conditions = models.TextField()