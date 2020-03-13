from rest_framework import generics
from .serializers import FileUploadSerializer, KeyPairSerializer
from .models import File, KeyPair


class FileListAndCreate(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer


class FileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer


class KeyPairListAndCreate(generics.ListCreateAPIView):
    queryset = KeyPair.objects.all()
    serializer_class = KeyPairSerializer


class KeyPairDetails(generics.RetrieveDestroyAPIView):
    queryset = KeyPair.objects.all()
    serializer_class = KeyPairSerializer
