from django.urls import path

from . import views

urlpatterns = [
    path('files/', views.FileListAndCreate.as_view()),
    path('files/<int:pk>/', views.FileDetails.as_view()),
    path('keys/', views.RSAKeyPairCreate.as_view()),
    path('certificates/create/', views.CertificateCreation.as_view()),
    path('certificates/', views.CertificatesList.as_view())
]
