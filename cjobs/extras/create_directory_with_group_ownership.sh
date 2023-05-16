function create_directory_with_group_ownership() {
    directory=$1
    gid=$2
    parent_directory=$(dirname "$directory")
    lock_file="$parent_directory/permissions.lock"
    max_wait_time=$((2 * 60))
    wait_time=0

    # Helper function to acquire the lock
    acquire_lock() {
        exec 3>"$lock_file"
        flock -n 3
        echo "Successfully acquired lock."
    }

    # Helper function to release the lock
    release_lock() {
        exec 3>&-
        rm "$lock_file"
        echo "The lock has been released."
        
    }

    # Creates the parent directory if it doesn't exist
    if [ ! -d "$parent_directory" ]; then
        mkdir -p "$parent_directory"
    fi

    echo "Attempting to acquire lock for setting folder permissions."

    # Attempt to acquire the lock
    while ! acquire_lock; do
        echo "Waiting for the lock to be released..."
        sleep 5
        wait_time=$((wait_time + 5))
        if [ "$wait_time" -gt "$max_wait_time" ]; then
            echo "Maximum wait time exceeded. Exiting..."
            exit 1
        fi
    done

    echo "Successfully acquired lock to set folder permissions."

    # Check if the directory exists
    if [ ! -d "$directory" ]; then
        # Create the directory
        mkdir -p "$directory"

        # Change the group ownership by GID
        chown -R :"$gid" "$parent_directory"
        chmod -R 770 "$parent_directory"

        echo "Directory created: $directory"
        echo "Group ownership set to GID: $gid"
        echo "Permissions set to rwx for owner and group, and none for others."

    else
        echo "Directory already exists: $directory"
        directory_owner=$(stat -c "%U" "$parent_directory")

        if [ "$USER" = "$directory_owner" ]; then
            echo "The user $USER is the owner of the directory $parent_directory. Applying standard permission settings"

            # Change the group ownership by GID
            chown -R :"$gid" "$parent_directory"
            chmod -R 770 "$parent_directory"
        else
            echo "The user $USER is not the owner of the directory $parent_directory. There is nothing to do"
            release_lock
            return
        fi
    fi

    # Release the lock
    release_lock
}