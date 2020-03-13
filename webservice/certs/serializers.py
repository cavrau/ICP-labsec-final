from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import File, KeyPair
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class FileUploadSerializer(serializers.ModelSerializer):
    sha_256 = serializers.CharField(allow_blank=True)
    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        sha256_hash = hashlib.sha256()
        [sha256_hash.update(byte_block) for byte_block in iter(lambda: validated_data['archive'].read(4096),b"")]
        validated_data['sha_256'] = sha256_hash.hexdigest()
        return File.objects.create(**validated_data)

    def update(self, instance: File, validated_data):
        archive = validated_data.get('archive', None)
        if archive is None:
            raise ValidationError('Archive can\'t be null if you are updating the file')
        sha256_hash = hashlib.sha256()
        [sha256_hash.update(byte_block) for byte_block in iter(lambda: archive.read(4096),b"")]
        validated_data['sha_256'] = sha256_hash.hexdigest()
        return super(FileUploadSerializer, self).update(instance, validated_data)

class KeyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPair
        fields = '__all__'

    def create(self, validated_data):
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
        ).decode('utf-8')
        public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        ).decode('utf-8')
        return KeyPair.objects.create(public_key=public_key, private_key=private_key)



