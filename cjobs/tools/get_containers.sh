function get_containers() {
  containers_dir="$1"
  requested_container="$2"
  if [[ ! -d $containers_dir ]]; then
    mkdir $containers_dir
    rclone cp "$requested_container" "$container_dir"
  else
    if [[ ! -e "$containers_dir"/"$requested_container" ]]; then
      rclone copy "$requested_container" "$container_dir"
    fi
  fi    
}