from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto")

def get_password_hash(password: str) -> str:
    """
        Hashes the password using bcrypt.

        :param password: Password
        :return: Hashed password
    """
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Verifies the password using bcrypt.

        :param plain_password: Password
        :param hashed_password: Hashed password
        :return: True if the password is correct, False otherwise
    """
    return bcrypt_context.verify(plain_password, hashed_password)
