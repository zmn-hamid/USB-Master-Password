import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from GetUUID import get_uuid


passphrase = get_uuid()


# Function to derive a key from a passphrase
def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))


# Generate a salt
salt = os.urandom(16)

# Derive a key from the passphrase
key = derive_key(passphrase, salt)

# Initialize Fernet with the derived key
fernet = Fernet(key)

# Your master password
master_password = input("enter your master password and press enter: ")

# Encrypt the master password
encrypted = fernet.encrypt(master_password.encode())

# Save the encrypted password and salt to your flash drive
with open("enc_mp.bin", "wb") as f:
    f.write(encrypted)
with open("enc_salt.bin", "wb") as f:
    f.write(salt)
