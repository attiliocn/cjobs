function acquire_lock() {
    local lock_name=$1
    local lock_location=$2
    local lock_file="$lock_location/$lock_name"

    exec 3>"$lock_file"
    if flock -n -e 3; then
        echo "Successfully acquired lock for $lock_name at $lock_location."
        return 0
    else
        return 1
    fi
}
function release_lock() {
    local lock_name=$1
    local lock_location=$2
    local lock_file="$lock_location"/"$lock_name"
    
    exec 3>&-
    rm "$lock_file"
    echo "The lock for $lock_name at $lock_location has been released."
}
function attempt_acquire_lock() {
    local lock_name=$1
    local lock_location=$2
    local max_wait_time=$3
    local wait_time=0
    
    while ! acquire_lock "$lock_name" "$lock_location"; do
        echo "Waiting for the lock to be released..."
        sleep 5
        wait_time=$((wait_time + 5))
        if [ "$wait_time" -gt "$max_wait_time" ]; then
            echo "Maximum wait time exceeded. Exiting..."
            exit 1
        fi
    done
}