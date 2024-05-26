function fetch_containers_from_drive() {
    container_cloud_dir="$1"
    container_local_dir="$2"
    container_local_dir_parent=$(dirname "$container_local_dir")

    synced_file="$container_local_dir_parent/last_sync.lock"

    # Check if the synced file exists and is older than 1 week
    if [ -e "$synced_file" ]; then
        file_age=$(($(date +%s) - $(stat -c %Y "$synced_file")))

        if [ "$file_age" -lt 604800 ]; then
            echo "LOG: The last sync was done $file_age seconds ago. Actions will not be performed."
            return
        fi
    fi

    if ! command -v rclone &>/dev/null; then
        echo "LOG: The rclone command is unavailable. No synchronization will be performed."
        return
    fi
    echo "LOG: Updating containers directory using rclone"
    rclone sync -v "$container_cloud_dir" "$container_local_dir"

    touch "$synced_file"
    echo "LOG: Updated last_sync.lock file"
}