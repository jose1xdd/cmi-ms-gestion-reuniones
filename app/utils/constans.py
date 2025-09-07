from fastapi.security import HTTPBearer


AUTH_HEADER = "Authorization"
JSON_HEADER = {"Content-Type": "application/json"}
BEARER_SCHEME = HTTPBearer()