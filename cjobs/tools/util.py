import hashlib
import datetime
import os

def get_timestamp():
    current_time = datetime.datetime.now()
    return current_time.strftime('%Y-%m-%d_%H-%M-%S')

def get_hash_from_timestamp():
    ts = get_timestamp()
    return hashlib.sha1(ts.encode('utf-8')).hexdigest()

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False
    
def convert_hours_to_hhmmss(hours:float) -> str:
    duration = datetime.timedelta(hours=hours)
    totsec = duration.total_seconds()
    h = totsec//3600
    m = (totsec%3600) // 60
    sec =(totsec%3600)%60
    converted_time = f"{int(h):02d}:{int(m):02d}:{int(sec):02d}"
    return converted_time

def py_array_to_bash(arr:list):
    bash_arr = " ".join([f'"{i}"' for i in arr])
    return bash_arr