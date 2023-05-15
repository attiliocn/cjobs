function create_directory_with_group_ownership() {
    directory=$1 # a three level folder structure is expected like PARENT/f1/f2 
    gid=$2
    parent_directory=$(dirname "$directory") # refers to f1 in the strucuture above

    # Create the lock file
    lock_file="$parent_directory"/permissions.lock
    touch "$lock_file"
    echo "Lock file permissions.lock is placed"

    max_wait_time=$((2 * 60))  # 2 minutes in seconds
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
        
        # remove the lock file
        rm "$lock_file"
        echo "Lock file removed. Actions completed successfully."
    else
        echo "Directory already exists: "$directory"."
        directory_owner=$(stat -c "%U" "$parent_directory")

        if [ $USER = $directory_owner ]; then
            echo "The user $USER is the owner of the directory "$parent_directory". Applying standard permission settings"
            
            # Change the group ownership by GID
            chown -R :"$gid" "$parent_directory"
            chmod -R 770 "$parent_directory"
            
            # remove the lock file
            rm "$lock_file"
            echo "Lock file removed. Actions completed successfully."
        else
            echo "The user $USER is not the owner of the directory "$parent_directory". There is nothing to do"

            # remove the lock file
            rm "$lock_file"
            echo "Lock file removed. Actions completed successfully."
            return
        fi
    fi
}