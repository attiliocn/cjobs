import subprocess

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