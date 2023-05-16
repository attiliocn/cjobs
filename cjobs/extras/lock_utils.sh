acquire_lock() {
    local lock_name=$1
    local lock_location=$2
    local lock_file="$lock_location"/"$lock_name"
    
    exec 3>"$lock_file"
    flock -n 3
    echo "Successfully acquired lock for $lock_name at $lock_location."
}

release_lock() {
    local lock_name=$1
    local lock_location=$2
    local lock_file="$lock_location"/"$lock_name"
    
    exec 3>&-
    rm "$lock_file"
    echo "The lock for $lock_name at $lock_location has been released."
}
