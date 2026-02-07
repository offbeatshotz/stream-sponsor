import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(stream_key: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """Derives a 32-byte key from a stream key for Fernet encryption."""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(stream_key.encode()))
    return key, salt

def encrypt_data(data: str, stream_key: str) -> str:
    """Encrypts data using the stream key and returns a URL-safe string."""
    key, salt = derive_key(stream_key)
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    # Prepend salt to the encrypted data so it can be used for decryption
    combined = salt + encrypted_data
    return base64.urlsafe_b64encode(combined).decode()

def decrypt_data(encrypted_bundle: str, stream_key: str) -> str:
    """Decrypts a bundle using the stream key."""
    try:
        decoded_bundle = base64.urlsafe_b64decode(encrypted_bundle.encode())
        salt = decoded_bundle[:16]
        encrypted_data = decoded_bundle[16:]
        
        key, _ = derive_key(stream_key, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

if __name__ == "__main__":
    # Test
    sk = "live_123456789_abcdefg"
    payload = '{"type": "youtube", "user": "StreamerName", "overlay_config": {"color": "red"}}'
    
    encrypted = encrypt_data(payload, sk)
    print(f"Encrypted: {encrypted}")
    
    decrypted = decrypt_data(encrypted, sk)
    print(f"Decrypted: {decrypted}")
