from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/details', views.edit_details, name='edit_details'),
    path('edit/designation', views.edit_designation, name='edit_designation'),
    path('edit/profile', views.profile_pic, name='profile_pic'),

    url(r'^files/', include('db_file_storage.urls')),
]
