
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import os
from .models import Certificate

one_day = datetime.timedelta(1, 0, 0)


class Certifier():
    def __init__(self):
        with open("private_key.pem", "rb") as key_file:
            self.private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key() 
        if os.path.isfile('.cert/certificate.pem'):
            with open('.cert/certificate.pem') as _cert:
                self.certificate = x509.load_pem_x509_certificate(_cert.read(), default_backend())
        else:
            self.auto_sing()
        
    def auto_sing(self):
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME,  u'LABSEC-Gabriel-AC'),
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'LABSEC-Gabriel-AC'),
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(self.public_key)
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        self.certificate =  builder.sign(
            private_key=self.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )
        with open('.cert/certificate.pem') as _cert:
            _cert.write(self.certificate.public_bytes())      

    def sign(self, subject_name, public_key):
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'{}'.format(subject_name)),
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'LABSEC-Gabriel-AC'),
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(public_key)
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        certificate =  builder.sign(
            private_key=self.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend()
        )
        certificate.serial_number
        certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        certificate.public_bytes(encoding=serialization.Encoding.PEM).decode('utf-8')
        return certificate
