import os
from pathlib import Path

from pymongo import MongoClient
from pymongo.errors import PyMongoError


def load_env_file() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env_file()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://dianakov_db_user:QhlttWmzwksqA7yY@habitcluster1.yzrxxet.mongodb.net/")
# Add tlsAllowInvalidCertificates for development
if "tlsAllowInvalidCertificates" not in MONGODB_URI and "mongodb+srv" in MONGODB_URI:
    MONGODB_URI += "?tlsAllowInvalidCertificates=true&retryWrites=true&w=majority"
elif "mongodb+srv" not in MONGODB_URI:
    # For local MongoDB
    pass

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "habitplatform")
MONGODB_TIMEOUT_MS = int(os.getenv("MONGODB_TIMEOUT_MS", "5000"))

client = None
db = None


def get_database():
    global client, db
    if client is None or db is None:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=MONGODB_TIMEOUT_MS)
        db = client[MONGODB_DB_NAME]
    return db


def ping_database() -> bool:
    try:
        current_client = client
        if current_client is None:
            get_database()
            current_client = client
        current_client.admin.command("ping")
    except PyMongoError:
        return False
    return True


def get_collection(name: str):
    return get_database()[name]
