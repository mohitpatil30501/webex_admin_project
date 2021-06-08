from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.webex_panel, name='webex_panel'),
    path('team/create', views.team_create, name='team_create'),
    path('team/attendance/<str:meeting_id>', views.team_attendance, name='team_attendance'),
    path('team/admit/<str:meeting_id>', views.team_admit, name='team_admit'),
    path('team/<str:meeting_id>/edit', views.team_edit, name='team_edit'),
    path('team/<str:meeting_id>/delete', views.team_delete, name='team_delete'),
    path('team/member/<str:membership_id>/delete', views.team_member_delete, name='team_member_delete'),
    path('team/member/<str:meeting_id>/add', views.team_member_add, name='team_member_add'),
    path('team/member/<str:meeting_id>/add/list', views.team_member_add_list, name='team_member_add_list'),
]
