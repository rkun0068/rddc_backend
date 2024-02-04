from django.contrib import admin
from django.urls import path
from model import views

urlpatterns = [
    path('detectImage', views.detect_and_save_images),
    path('detectVideo', views.detect_and_save_video),
    path('detectInfo', views.get_detection_info),
    path('detectReal',views.realtime_detect)
]
