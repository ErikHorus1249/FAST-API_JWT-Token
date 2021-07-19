
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


plain_pass = "admin"
hashed_pass = get_password_hash(plain_pass)
print(hashed_pass)
print(verify_password(plain_pass, get_password_hash(plain_pass)))

# print(get_password_hash("secret"))