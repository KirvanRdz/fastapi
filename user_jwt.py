import jwt

def create_token(data:dict):
    token: str = jwt.encode(data, "secret", algorithm="HS256")
    return token

def validate_token(token:str)->dict:
    token: str = jwt.decode(token,key="secret",algorithms=["HS256"])
    return token