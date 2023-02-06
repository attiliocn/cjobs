import hashlib
from datetime import datetime

def get_timestamp():
    current_time = datetime.now()
    return current_time.strftime('%Y-%m-%d_%H-%M-%S')

def get_hash_from_timestamp(timestamp):
    ts = get_timestamp()
    return hashlib.sha1(ts.encode('utf-8')).hexdigest()