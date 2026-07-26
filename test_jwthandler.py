from app.jwt_handler import create_access_token, verify_access_token
import jwt

token = create_access_token(1)
print(token)
print("Payload", verify_access_token(token))

