from django.contrib import admin
from . models import Ashaworker
from . models import Appointment
from . models import Image
from . models import CustomUser
from . models import PatientProfile


admin.site.register(Ashaworker)
admin.site.register(Appointment)
admin.site.register(Image)
admin.site.register(CustomUser)
admin.site.register(PatientProfile)



# Register your models here.
