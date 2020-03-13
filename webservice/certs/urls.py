from django.urls import path

from . import views

urlpatterns = [
    path('files/', views.FileListAndCreate.as_view()),
    path('files/<int:pk>/', views.FileDetails.as_view()),
    path('keys/', views.KeyPairListAndCreate.as_view()),
    path('keys/<int:pk>/', views.KeyPairDetails.as_view()),
]