# urls.py
from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
       # All tickets
    path('tickets/', views.all_tickets, name='all_tickets'),
    # Index
    path('index/', views.lobby, name='index'),
    # Index (Changing streaming camera)
    path('index/<str:filter>/', views.lobby, name='index'),

    # Webcam recording
    path('webcam/', views.webcam, name='webcam'),

    #Optimize the webcam recording
     path('optimize/', views.optimize, name='optimize'),

    # Contact us
    path('ticket/', views.contact, name='contact'),
 

    # Camera list
    path('cameras/', views.cameras, name='cameras'),
    # Camera add
    path('camera/', views.camera, name='camera'),
    # Camera edit
    path('camera/<str:id>', views.camera, name='camera'),
    # Camera edit screen
    path('camera/edit/<str:id>', views.camera, name='camera'),
    # Camera delete
    path('camera/delete/<str:id>', views.camera_del, name='camera_del'),

    # Statistics
    path('data/', views.data, name='data'),
    # Statistics filter
    path('data/<str:filter>/', views.data, name='data'),

    # Video
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('video/<int:id>', views.video, name='video'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
