function create_directory_with_group_ownership() {
    directory=$1 # a three level folder structure is expected like PARENT/f1/f2 
    gid=$2
    parent_directory=$(dirname "$directory") # refers to f1 in the strucuture above

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
        echo "Directory already exists: "$directory". Only the permissions settings will be applied"
        # Change the group ownership by GID
        chown -R :"$gid" "$parent_directory"
        chmod -R 770 "$parent_directory"
    fi
}