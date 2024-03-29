function create_directory_with_group_ownership() {
    directory=$1
    gid=$2
    parent_directory=$(dirname "$directory")

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
            return
        fi
    fi
}