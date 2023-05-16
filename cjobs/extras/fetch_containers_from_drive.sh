function fetch_containers_from_drive() {
    container_cloud_dir="$1"
    container_local_dir="$2"
    container_local_dir_parent=$(dirname "$container_local_dir") 
    
    lock_file="$container_local_dir_parent"/rclone.lock
    synced_file="$container_local_dir_parent"/last_sync.lock

    max_wait_time=$((30 * 60))  # 30 minutes in seconds
    wait_time=0

    echo "Attempting to acquire lock for RClone usage."
    # Attempt to acquire the lock
    while true; do
        exec 3>"$lock_file"
        if flock -n 3; then
        echo "Successfully acquired lock for for RClone usage."
            break
        fi
        echo "Waiting for the lock to be released..."
        sleep 5
        wait_time=$((wait_time + 5))
        if [ "$wait_time" -gt "$max_wait_time" ]; then
                echo "Maximum wait time exceeded. Exiting..."
                exit 1
            fi
    done
    
    # Check if the synced file exists and is older than 1 week
    if [ -e "$synced_file" ]; then
        file_age=$(($(date +%s) - $(stat -c %Y "$synced_file")))

        if [ "$file_age" -lt 604800 ]; then
            echo "The last sync was done "$file_age" seconds ago. Actions will not be performed."
            # Release the lock
            exec 3>&-
            echo "The lock has been released."
            return
        fi
        
    fi

    if [[ ! -x  "$(command -v rclone)" ]]; then
        echo "The rclone command is unavailable. No synchronization will be performed."
        # Release the lock
        exec 3>&-
        echo "The lock has been released."
        return
    fi
  
    rclone sync -v "$container_cloud_dir" "$container_local_dir"
    # Release the lock
    exec 3>&-
    echo "The lock has been released."
    touch $synced_file
    echo "Updated last_sync.lock file"
    
}
