function clean_job() {
  echo "Received SIG"
  if [[ -d "$job_scratch_dir" ]]; then
    echo "Copying outputs to local_dir"
    cp -vr "$job_scratch_dir" "$job_local_dir"
    echo "Removing scratch dir"
    rm -vrf "$job_scratch_dir"
    echo "Job done"
    echo ""
  else
    echo "scratch dir does not exist"
    echo ""
  fi
  exit
}
trap clean_job EXIT HUP INT TERM ERR