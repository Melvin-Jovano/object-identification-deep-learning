from dotenv import dotenv_values

CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
DEBUG_MODE = True if dotenv_values(".env")['DEBUG_MODE'] == "true" else False