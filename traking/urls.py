from django.urls import path
from .views import create_tracked_link,track_click,tracked_link_detail

urlpatterns = [
    path('create/', create_tracked_link, name='create_tracked_link'),
    path('r/<slug:slug>/', track_click, name='track_click'),  # Shortened URL endpoint
    path('detail/<int:pk>/', tracked_link_detail, name='tracked_link_detail'),
]
