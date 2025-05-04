import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data') 