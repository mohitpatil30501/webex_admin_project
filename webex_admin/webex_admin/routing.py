from django.urls import path

from User.consumers import *
from Dashboard.consumers import *

websocket_urlpatterns = [
    path('user/<str:id>', UserConsumer.as_asgi()),
    path('user/reset_password/<str:id>', UserResetPasswordConsumer.as_asgi()),
    path('details/<str:id>', DetailsConsumer.as_asgi()),
    path('designation/<str:id>', DesignationConsumer.as_asgi()),
]
