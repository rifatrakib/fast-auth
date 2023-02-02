from server.security.hash import hash_generator


class PasswordGenerator:
    @property
    def generate_salt(self) -> str:
        return hash_generator.generate_salt_hash

    def generate_hashed_password(self, hash_salt: str, password: str) -> str:
        return hash_generator.generate_password_hash(hash_salt=hash_salt, password=password)

    def verify_password(self, hash_salt: str, password: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(password=hash_salt + password, hashed_password=hashed_password)


def get_password_generator() -> PasswordGenerator:
    return PasswordGenerator()


pwd_generator: PasswordGenerator = get_password_generator()
