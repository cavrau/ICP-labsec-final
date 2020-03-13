from django.db import models

# Create your models here.

class File(models.Model):   
    archive = models.FileField(null=False, upload_to='webservice/archives')
    sha_256 = models.CharField(max_length=256)

class KeyPair(models.Model):
    public_key = models.CharField(max_length=2048)
    private_key = models.CharField(max_length=2048)

class Certificate(model.Model):
    subject = models.CharField()
    serial_number = models.CharField()
    issuer = models.CharField()
    certificate = models.CharField()
