from django.http import HttpResponseForbidden
from .models import CustomUser

def ashaworker_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has the "ashaworker" role
        if request.user.is_authenticated and request.user.role == CustomUser.ASHAWORKER:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied")

    return _wrapped_view

def patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and has the role "patient"
        if request.user.is_authenticated and request.user.role == "patient":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Permission Denied")

    return _wrapped_view