def build_scheduler_header(scheduler, job_name, n_cores, memory, job_time, n_jobs=1, job_array=False):
    scheduler_header = []
    if scheduler == 'slurm':
        scheduler_header.append(f"#SBATCH --job-name {job_name}")
        scheduler_header.append(f"#SBATCH --output=job_%x_%J.stdout")
        scheduler_header.append(f"#SBATCH --nodes=1")
        scheduler_header.append(f"#SBATCH --ntasks={n_cores}")
        scheduler_header.append(f"#SBATCH --mem-per-cpu={memory}")
        scheduler_header.append(f"#SBATCH --time={job_time}")
        if n_jobs > 1 and job_array == True:
            scheduler_header.append(f"#SBATCH --array=1-{n_jobs}")
        scheduler_header.append(f"#SBATCH --signal=B:TERM@60")
    elif scheduler == 'pbs-pro':
        scheduler_header.append(f'#PBS -N {job_name}')
        scheduler_header.append(f'#PBS -o {job_name}.stdout')
        scheduler_header.append(f'#PBS -e {job_name}.stderr')
        scheduler_header.append(f'#PBS -l select=1:ncpus={n_cores}:mem={n_cores*memory}mb')
        scheduler_header.append(f'#PBS -l walltime={job_time}')
        if n_jobs > 1 and job_array == True:
            scheduler_header.append(f'#PBS -J 1-{n_jobs}:1')
    else:
        return None
    return scheduler_header

def get_scheduler_variables(scheduler):
    scheduler_vars = {}
    if scheduler == 'slurm':
        scheduler_vars['job_id'] = '$SLURM_JOB_ID'
        scheduler_vars['array_task_id'] = '$SLURM_ARRAY_TASK_ID'
    elif scheduler == 'pbs-pro':
        scheduler_vars['job_id'] = '$PBS_JOBID'
        scheduler_vars['array_task_id'] = '$PBS_ARRAY_INDEX'
    else:
        return None
    return scheduler_vars
    