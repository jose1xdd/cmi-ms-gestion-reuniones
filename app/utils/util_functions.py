import secrets
import string
def generate_code(length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits  # A-Z and 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))
