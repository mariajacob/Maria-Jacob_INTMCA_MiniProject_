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
        user.role=6
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    PATIENTS = 1
    ASHAWORKER = 2
    HCA = 3
    ADMIN = 4
    NURSE=5
    MEMBER=6

    ROLE_CHOICE = (
        ( PATIENTS, ' PATIENTS'),
        (ASHAWORKER, 'ASHAWORKER'),
        (HCA, 'HCA'),
        (ADMIN,'ADMIN'),
        (NURSE,'NURSE'),
        (MEMBER,'MEMBER'),
    
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ashaworker')
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
    ward = models.CharField(max_length=100,blank=True, null=True)
    
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
    reset_password = models.CharField(max_length=128, null=True, blank=True)  # New field for reset password
    is_active = models.BooleanField(default=True)
    
    class Meta:
            unique_together = (("id", "ward"),)
    # pin = models.IntegerField()
    # bio=models.TextField()

    def _str_(self):
        return self.Name



class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    Name = models.CharField(max_length=100)
    
    email = models.EmailField(blank=True, null=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, password):
        # Hash and set the password
        self.admin_set_password = make_password(password)
    
    
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    taluk = models.CharField(max_length=100)
    Panchayat = models.CharField(max_length=100)
    wardmem = models.IntegerField(max_length=100,blank=True, null=True)
    
    
    phone = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    
    reset_password = models.CharField(max_length=128, null=True, blank=True)  # New field for reset password
    is_active = models.BooleanField(default=True)
    
    class Meta:
            unique_together = (("id", "wardmem"),)
    # pin = models.IntegerField()
    # bio=models.TextField()

    def _str_(self):
        return self.Name   






class AshaworkerSchedule(models.Model):
    # Reference to the Ashaworker
    ashaworker = models.ForeignKey(Ashaworker, on_delete=models.CASCADE, related_name='schedules')

    # Available Days
    available_days = models.CharField(max_length=10, choices=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])

    # Start and End Time
    preferred_date = models.DateField(null=True,blank=True)
    preferred_time = models.CharField(max_length=20, choices=[('09:00AM', '09:00AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), ('01:00 PM', '01:00 PM')],null=True,blank=True)

    def __str__(self):
        return f'Schedule for {self.ashaworker.Name} ({self.available_days})'






    
class Image(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery/')  # 'gallery/' is the directory where images will be stored
    is_enabled = models.BooleanField(default=True) 
    def __str__(self):
        return self.title
    


class PatientProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    birth_date = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')],null=True,blank=True)
    house_name = models.CharField(max_length=100, null=True,blank=True)
    house_no = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    # ward = models.CharField(max_length=100)
    ward = models.CharField(max_length=50, choices=[('ward1', 'Ward 1-VENGATHANAM'),
    ('ward2', 'Ward 2-PALAPRA'),
    ('ward3', 'Ward 3-VELICHIYANI'),
    ('ward4', 'Ward 4-CHOTTY'),
    ('ward5', 'Ward 5-MANGAPPARA'),
    ('ward6', 'Ward 6-VADAKKEMALA'),
    ('ward7', 'Ward 7-PARATHODU'),
    ('ward8', 'Ward 8-NADUKANI'),
    ('ward9', 'Ward 9-EDAKKUNNAM'),
    ('ward10', 'Ward 10-KOORAMTHOOKKU'),
    ('ward11', 'Ward 11-KOOVAPPALLY'),
    ('ward12', 'Ward 12-KULAPPURAM'),
    ('ward13', 'Ward 13-PALAMPRA'),
    ('ward14', 'Ward 14-MUKKALY'),
    ('ward15', 'Ward 15-PODIMATTAM'),
    ('ward16', 'Ward 16-ANAKKALLU'),
    ('ward17', 'Ward 17-PULKUNNU'),
    ('ward18', 'Ward 18-PAZHUMALA'),
    ('ward19', 'Ward 19-CHIRABHAGAM'),],null=True,blank=True)
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
    is_active = models.BooleanField(default=True,null=True,blank=True)
    
    def _str_(self):
        return self.first_name



class Slots(models.Model):
    ashaworker = models.ForeignKey(Ashaworker, on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # def _str_(self):
    #     return f"Slot for Ashaworker. {self.ashaworker.Name} on {self.date} at {self.start_time}-{self.end_time}"
    def __str__(self):
        return f"Slot for Ashaworker {self.ashaworker.Name} on {self.date} at {self.start_time}-{self.end_time}"

class Appointment(models.Model):
   
    is_approved=models.BooleanField(default=False)
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    # date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    ward_asha = models.CharField(max_length=255,null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    # id_proof = models.FileField(upload_to='id_proofs/',null=True,blank=True)
    medical_conditions = models.TextField(null=True,blank=True)
    urgency = models.CharField(max_length=50, choices=[('Routine check-up', 'Routine check-up'), ('Non-urgent medical check-up', 'Non-urgent medical check-up'), ('Urgent medical check-up', 'Urgent medical check-up')],null=True,blank=True)
    medication_names = models.TextField(null=True,blank=True)
    symptoms = models.TextField(null=True,blank=True)
    # preferred_date = models.DateField(null=True,blank=True)
    # preferred_time = models.CharField(max_length=20, choices=[('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), ('01:00 PM', '01:00 PM')],null=True,blank=True)

    ashaworker = models.ForeignKey(Ashaworker, on_delete=models.CASCADE, related_name='appointments',blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.ForeignKey(Slots,on_delete=models.CASCADE,null=True,blank=True)
    
    date = models.DateField(blank=True, null=True)
    status=models.BooleanField(default=True,blank=True, null=True)

    def __str__(self):
        return self.email

#     def __str__(self):
#         return self.email

# class MedicalRecord(models.Model):
#     first_name = models.CharField(max_length=255,null=True,blank=True)
#     last_name = models.CharField(max_length=255,null=True,blank=True)
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     date = models.DateField()
#     doctor_notes = models.TextField()
#     medications_needed = models.TextField()
#     treatments = models.TextField()
#     current_conditions = models.TextField()

class MedicalRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    
    date = models.DateField( null=True, blank=True)
    doctor_notes = models.TextField( null=True, blank=True)
    medications_needed = models.TextField( null=True, blank=True)
    treatments = models.TextField( null=True, blank=True)
    current_conditions = models.TextField( null=True, blank=True)


class home_visit(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    date = models.DateField( null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.email
    



class Donation(models.Model):
    donor_name = models.CharField(max_length=255)
    email = models.EmailField()
    donor_place = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    # order=models.CharField(max_length=255,blank=True, null=True)
    def __str__(self):
        return self.donor_name



    


class Blog(models.Model):
    author=models.CharField(max_length=200, null=True,blank=True)
    title = models.CharField(max_length=200, verbose_name='Blog Name')
    images = models.ImageField(upload_to='blog_images/', verbose_name='Blog Images', null=True, blank=True)
    category = models.CharField(max_length=100,choices = [('Health Care','Health Care'), ('Child', 'Child'),('Technology', 'Technology')])
    blog_date = models.DateField(null=True,blank=True)
    # sub_category = models.CharField(max_length=100, verbose_name='Blog Sub Category')
    description = models.TextField(verbose_name='Blog Description')
    # tags = models.CharField(max_length=200, verbose_name='Tags', help_text='Separated with a comma')
    
    def __str__(self):
        return self.title

class Hca(models.Model):
     
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    
    hcaname = models.CharField(max_length=100)
    
    email = models.EmailField(blank=True, null=True)
    admin_set_password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, password):
        # Hash and set the password
        self.admin_set_password = make_password(password)
    
    date_of_join = models.CharField(max_length=100)
    
    
    address = models.TextField()
    taluk = models.CharField(max_length=100)
    panchayat = models.CharField(max_length=100)
    
    
    postal = models.IntegerField()
    phone = models.IntegerField()
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    
    license_certificate=models.FileField(upload_to='lic_cert/', blank=True, null=True)
    
    year_hca=models.IntegerField(blank=True, null=True)
    

    is_active = models.BooleanField(default=True)
    
   

    def _str_(self):
        return self.hcaname
