function clean_job() {
    echo "NOTICE: Received signal. The trap has been activated."
    if [[ -d "$job_scratch_dir" ]]; then
        echo "Copying outputs to local directory."
        cp -vr "$job_scratch_dir" "$job_local_dir"/"$job_name"
        echo "Successfully copied outputs."
        echo "Removing scratch directory."
        rm -vrf "$job_scratch_dir"
        echo "Scratch directory removed."
        echo "Job completed."
        echo ""
    else
        echo "Scratch directory does not exist."
        echo ""
    fi
    exit
}