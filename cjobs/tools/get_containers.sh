function get_containers() {
  container_cloud_dir="$1"
  container_local_dir="$2"
  if [[ ! -x  "$(command -v rclonador)" ]]; then
    echo "rclone not found"
    echo "make sure to copy containers to container_dir manually"
    return
  elif [[ ! -d $container_local_dir ]]; then
    mkdir $container_local_dir
  fi    
  rclone sync -v "$container_cloud_dir" "$container_local_dir"
  return
}