def build_scheduler_header(scheduler, job_name, n_cores, memory, job_time, n_jobs=1):
    scheduler_header = []
    if scheduler == 'slurm':
        scheduler_header.append(f"#SBATCH --job-name {job_name}")
        scheduler_header.append(f"#SBATCH --output=job_%x_%A.stdout")
        scheduler_header.append(f"#SBATCH --nodes=1")
        scheduler_header.append(f"#SBATCH --ntasks={n_cores}")
        scheduler_header.append(f"#SBATCH --mem-per-cpu={memory}")
        scheduler_header.append(f"#SBATCH --time={job_time}")
        if n_jobs > 1:
            scheduler_header.append(f"#SBATCH --array=1-{n_jobs}")
        scheduler_header.append(f"#SBATCH --signal=B:TERM@60")
    else:
        return None
    return scheduler_header