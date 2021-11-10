import jwt

PAYLOAD = {"": ""}
SECRET = ""
DEFAULT_ALGO = "HS256"
ALGOS = [DEFAULT_ALGO]


def encode_jwt(payload=PAYLOAD, secret=SECRET, algorithm=DEFAULT_ALGO):
    """Encode a JWT by using the payload, secret and the algorithm"""
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(encoded_jwt, secret=SECRET, algorithms=ALGOS):
    """Encode a JWT by using the payload, secret and the algorithm"""
    return jwt.decode(encoded_jwt, secret, algorithms=algorithms)


jwt = encode_jwt()
print(jwt)
