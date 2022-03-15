from django.urls import path
from .views import *

app_name='noteapp'


urlpatterns =[

    path('signup',SignupAPIView.as_view(),name='signup'),
    path('login',LoginAPIView.as_view(),name='LoginView'),
    path('note',CRDNoteApiView.as_view(),name='note'),
    path('note/<int:pk>',CRDNoteApiView.as_view(),name='note1'),
    path('note2/<int:pk>',UpdateNoteApi.as_view(),name='update'),
    path('create_profile',AsdfView.as_view(),name='create_profile'),
    path('profiles',ProfileView.as_view(),name='profiles'),
    path('profiles/<int:pk>',ProfileView.as_view(),name='profiles'),
    
    ]