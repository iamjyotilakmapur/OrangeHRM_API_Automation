import os

try:
    from Config import BASE_URL as LOCAL_BASE_URL, TOKEN as LOCAL_TOKEN
except ImportError:
    LOCAL_BASE_URL = None
    LOCAL_TOKEN = None

BASE_URL = os.getenv("BASE_URL", LOCAL_BASE_URL)
TOKEN = os.getenv("TOKEN", LOCAL_TOKEN)