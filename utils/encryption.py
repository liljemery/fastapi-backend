import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # type: ignore[import-untyped]
from cryptography.hazmat.primitives import hashes  # type: ignore[import-untyped]
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # type: ignore[import-untyped]
from cryptography.hazmat.backends import default_backend  # type: ignore[import-untyped]
from config import settings

class AESUtility:
    def __init__(self, password: str) -> None:
        self.password = password.encode()

        self.salt = base64.b64decode(settings.ENCRYPTION_SALT)
        self.iv = base64.b64decode(settings.INIT_VECTOR)

        self.key = self.derive_key()

    def derive_key(self) -> bytes:
        """Derive a 32-byte key using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.password)

    def encrypt(self, plaintext: str) -> str:
        """Encrypt a plaintext string using AES-GCM."""
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()

        return base64.b64encode(json.dumps({
            'salt': base64.b64encode(self.salt).decode(),
            'iv': base64.b64encode(self.iv).decode(),
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }).encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt an encrypted string using AES-GCM."""
        decoded_data = json.loads(base64.b64decode(encrypted_data).decode())

        iv = base64.b64decode(decoded_data['iv'])
        ciphertext = base64.b64decode(decoded_data['ciphertext'])
        tag = base64.b64decode(decoded_data['tag'])

        key = self.derive_key()

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        return (decryptor.update(ciphertext) + decryptor.finalize()).decode()


aes_util = AESUtility(settings.SECRET_KEY)