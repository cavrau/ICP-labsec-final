from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import File, Certificate
import hashlib


class FileUploadSerializer(serializers.ModelSerializer):
    sha_256 = serializers.CharField(allow_blank=True)

    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        sha256_hash = hashlib.sha256()
        [
            sha256_hash.update(byte_block) for byte_block in iter(
                lambda: validated_data['archive'].read(4096), b""
            )
        ]
        validated_data['sha_256'] = sha256_hash.hexdigest()
        return File.objects.create(**validated_data)

    def update(self, instance: File, validated_data):
        archive = validated_data.get('archive', None)
        if archive is None:
            raise ValidationError('Archive can\'t be null if you are updating the file')
        sha256_hash = hashlib.sha256()
        [sha256_hash.update(byte_block) for byte_block in iter(lambda: archive.read(4096), b"")]
        validated_data['sha_256'] = sha256_hash.hexdigest()
        return super(FileUploadSerializer, self).update(instance, validated_data)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"
