function fetch_containers_from_drive() {
    container_cloud_dir="$1"
    container_local_dir="$2"
    container_local_dir_parent=$(dirname "$container_local_dir") 
    
    lock_file="$container_local_dir_parent"/rclone.lock
    synced_file="$container_local_dir_parent"/last_sync.lock

    max_wait_time=$((30 * 60))  # 30 minutes in seconds
    wait_time=0

    # Check if the lock file exists
    if [ -e "$lock_file" ]; then
        echo "Lock file already exists. Another instance of the script may be running."
        while [ -e "$lock_file" ]; do
            if [ "$wait_time" -gt "$max_wait_time" ]; then
                echo "Maximum wait time exceeded. Exiting..."
                exit 1
            fi
            echo "Waiting for the lock to be released..."
            sleep 5
            wait_time=$((wait_time + 5))
        done
    fi
    
    # Check if the synced file exists and is older than 1 week
    if [ -e "$synced_file" ]; then
        file_age=$(($(date +%s) - $(stat -c %Y "$synced_file")))
        if [ "$file_age" -lt 604800 ]; then
            echo "The last sync was done "$file_age" seconds ago. Actions will not be performed."
            return
        fi
    fi

    if [[ ! -x  "$(command -v rclone)" ]]; then
        echo "The rclone command is unavailable. No synchronization will be performed."
        return
    fi

    # Create the lock file
    touch "$lock_file"
    echo "Lock file is placed"
  
    rclone sync -v "$container_cloud_dir" "$container_local_dir"
    
    rm "$lock_file"
    echo "Lock file removed. Actions completed successfully."
    touch $synced_file
    echo "Updated last_sync.lock file"
    
}
