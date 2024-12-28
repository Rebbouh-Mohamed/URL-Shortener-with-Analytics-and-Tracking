from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_overview, name='dashboard_overview'),
    path('link/<int:link_id>/', views.link_detail, name='link_detail'),
]
