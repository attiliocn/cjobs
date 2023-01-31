function get_containers() {
  containers_dir="$1"
  requested_container="$2"
  if [[ ! -d $containers_dir ]]; then
    mkdir $containers_dir
    rclone copy "$requested_container" "$containers_dir"
  else
    if [[ ! -e "$containers_dir"/"$requested_container" ]]; then
      rclone copy "$requested_container" "$containers_dir"
    fi
  fi    
}