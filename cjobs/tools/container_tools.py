import subprocess

###
import os
import time

def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False

def is_cached_containers_file_old(file_path, tolerance_days=7):
    if not file_exists(file_path):
        return True
    else:
        # Check if the cached file is more than 1 week old
        file_age = time.time() - os.path.getmtime(file_path)
        if file_age > (tolerance_days*24*60*60):  # t(seconds) = days * 24 h * 60 min * 60 sec
            return True
        else:
            return False

def show_cached_containers_file_contents(file_path):
    if file_exists(file_path):
        # Read and display the contents of the cached file
        with open(file_path, 'r') as file:
            contents = file.read()
            print(contents)

def request_containers_using_rclone(remote_path):
    cli_string = f"rclone lsf {remote_path} | grep .sif"
    process = subprocess.run(cli_string, capture_output=True, shell=True)
    stdout = process.stdout.strip().decode("utf-8")
    stderr = process.stderr.strip().decode("utf-8")
    return stdout, stderr

def parse_containers_list(containers_list):
    containers_list.sort()
    containers_parsed = {}
    for container in containers_list:
        img_basename, img_extension = container.rsplit('.',1)
        img_prefix, build_date, img_idx = img_basename.rsplit('_',2)

        containers_parsed[img_idx] = {
            'basename':img_basename,
            'file':f"{img_basename}.{img_extension}",
        }
    return containers_parsed