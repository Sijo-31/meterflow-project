from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Fix: ensure password is safe length
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    password = password[:72]
    return pwd_context.verify(password, hashed_password)