from django.urls import path
from .import views

urlpatterns = [
    
    # path('home/' ,views.home,name='login'),
    # path('signup/' ,views.home1,name='signup'),


    
    # 
    path('', views.index,name='index'),
    path('', views.admin_login,name='adlogin'),
    
]