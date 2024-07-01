function clean_job() {
    echo "LOG: Received signal. The trap has been activated."
    if [[ -d "$exeDir" ]]; then
        echo "LOG: Copying outputs to local directory."
        rsync -avh "$exeDir"/* "$localDir" --exclude '*.stdout' --exclude '*.stderr'
        echo "LOG: Successfully copied outputs."
        echo "LOG: Removing scratch directory."
        rm -vrf "$exeDir"
        echo "LOG: Scratch directory removed."
        echo "LOG: Job completed."
    else
        echo "LOG: Scratch directory does not exist."
    fi
    exit
}