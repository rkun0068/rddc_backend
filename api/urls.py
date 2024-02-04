from django.urls import path

from api import views

urlpatterns = [
    path('upload', views.upload_file),
    path('getImage', views.get_image),
    path('delete', views.delete_files),
    path('getVideoUrl',views.get_video_url)
]
