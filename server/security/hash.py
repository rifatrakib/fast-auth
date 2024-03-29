from passlib.context import CryptContext

from server.core.config import settings


class HashGenerator:
    def __init__(self):
        self._password_hash: CryptContext = CryptContext(
            schemes=[settings.PASSWORD_HASH_ALGORITHM],
            deprecated="auto",
        )
        self._salt_hash: CryptContext = CryptContext(
            schemes=[settings.SALT_HASH_ALGORITHM],
            deprecated="auto",
        )
        self._salt: str = settings.HASH_SALT

    @property
    def _get_hashing_salt(self) -> str:
        return self._salt

    @property
    def generate_salt_hash(self) -> str:
        """method to generate a hash from bcrypt to append to the user
        password."""
        return self._salt_hash.hash(secret=self._get_hashing_salt)

    def generate_password_hash(self, hash_salt: str, password: str) -> str:
        """method to add the password with the layer 1 bcrypt hash, before hash
        it for the second time using bcrypt algorithm."""
        return self._password_hash.hash(secret=hash_salt + password)

    def is_password_verified(self, password: str, hashed_password: str) -> bool:
        """method to decode password and verify whether it is the correct."""
        return self._password_hash.verify(secret=password, hash=hashed_password)


def get_hash_generator() -> HashGenerator:
    return HashGenerator()


hash_generator: HashGenerator = get_hash_generator()
