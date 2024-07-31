function clean_job() {
    echo "LOG: Received signal. The trap has been activated."
    if [[ -d "$exeDir" ]]; then
        echo "LOG: Copying outputs to local directory."
        cp -r "$exeDir"/*/ "$localDir"
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