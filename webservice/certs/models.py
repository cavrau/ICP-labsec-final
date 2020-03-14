from django.db import models

# Create your models here.


class File(models.Model):
    archive = models.FileField(null=False, upload_to=f'archives')
    sha_256 = models.CharField(max_length=256)


class Certificate(models.Model):
    subject = models.CharField(max_length=200000)
    serial_number = models.CharField(max_length=200000)
    subject_public_key = models.FileField(null=False, upload_to=f'keys')
    issuer = models.CharField(max_length=200000)
    certificate = models.FileField(null=False, upload_to=f'certificate')
