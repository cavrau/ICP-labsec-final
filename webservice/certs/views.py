import io
import zipfile
import json
import uuid
from rest_framework import generics
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.base import ContentFile

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from .serializers import FileUploadSerializer, CertificateSerializer
from .models import File, Certificate
from .certifier import Certifier
from cryptography.x509.oid import NameOID


class FileListAndCreate(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer


class FileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer


class CertificatesList(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class RSAKeyPairCreate(TemplateView):
    def get(self, request):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        )
        outfile = io.BytesIO()

        with zipfile.ZipFile(outfile, 'w') as zf:
            zf.filename = 'keys'
            zf.writestr("public-key.pem", public_key)
            zf.writestr("private-key.pem", private_key)
        return HttpResponse(outfile.getvalue(), content_type='application/zip')


class CertificateCreation(TemplateView):
    def post(self, request):
        certificate = Certifier().sign(request.POST['subject'], request.FILES['public_key'])
        cert_file = ContentFile(certificate.public_bytes(encoding=serialization.Encoding.PEM))
        public_key_file = ContentFile(
            certificate.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.PKCS1
            )
        )

        cert_file.name = f'certificate_{str(uuid.uuid4())}.pem'
        public_key_file.name = f'public_key_{request.POST["subject"]}_{str(uuid.uuid4())}.pem'
        cert = Certificate.objects.create(
            serial_number=certificate.serial_number,
            issuer=certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,
            subject=certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value,
            subject_public_key=public_key_file,
            certificate=cert_file
        )
        return HttpResponse(json.dumps(CertificateSerializer(cert).data), content_type='application/json')
