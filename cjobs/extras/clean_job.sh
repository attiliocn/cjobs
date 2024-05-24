function clean_job() {
    echo "NOTICE: Received signal. The trap has been activated."
    if [[ -d "$exeDir" ]]; then
        echo "Copying outputs to local directory."
        rsync -avh "$exeDir"/ "$localDir"
        echo "Successfully copied outputs."
        echo "Removing scratch directory."
        rm -vrf "$exeDir"
        echo "Scratch directory removed."
        echo "Job completed."
        echo ""
    else
        echo "Scratch directory does not exist."
        echo ""
    fi
    exit
}