import hashlib
from datetime import datetime
import os

def get_timestamp():
    current_time = datetime.now()
    return current_time.strftime('%Y-%m-%d_%H-%M-%S')

def get_hash_from_timestamp():
    ts = get_timestamp()
    return hashlib.sha1(ts.encode('utf-8')).hexdigest()

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False