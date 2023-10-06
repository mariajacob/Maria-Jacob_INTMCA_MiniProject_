from django.contrib import admin
from . models import Ashaworker
from . models import Appointment
from . models import Image
from . models import CustomUser
from . models import PatientProfile
from . models import MedicalRecord
from . models import Donation
from . models import AshaworkerSchedule
from . models import Slots
from . models import Blog
from . models import Hca







admin.site.register(Ashaworker)
admin.site.register(AshaworkerSchedule)
admin.site.register(Appointment)
admin.site.register(Image)
admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(MedicalRecord)
admin.site.register(Donation)
admin.site.register(Slots)
admin.site.register(Blog)
admin.site.register(Hca)




# Register your models here.
