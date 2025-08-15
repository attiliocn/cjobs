def build_scheduler_header(job:object):
    scheduler_header = []
    if job.scheduler == 'slurm':
        scheduler_header.append(f"#SBATCH --job-name {job.cjobsID}")
        scheduler_header.append(f"#SBATCH --output=cjobs_log_%x_%J.stdout")
        scheduler_header.append(f"#SBATCH --nodes=1")
        scheduler_header.append(f"#SBATCH --ntasks={job.cpu}")
        scheduler_header.append(f"#SBATCH --mem={job.ram * job.cpu}")
        scheduler_header.append(f"#SBATCH --time={job.time}")
        if job.isArray == True:
            scheduler_header.append(f"#SBATCH --array=1-{job.numJobs}")
        scheduler_header.append(f"#SBATCH --signal=B:TERM@60")
    elif job.scheduler == 'pbs-pro':
        scheduler_header.append(f'#PBS -N {job.cjobsID}')
        scheduler_header.append(f'#PBS -o {job.cjobsID}.stdout')
        scheduler_header.append(f'#PBS -e {job.cjobsID}.stderr')
        scheduler_header.append(f'#PBS -l select=1:ncpus={job.cpu}:mem={job.cpu*job.ram}mb')
        scheduler_header.append(f'#PBS -l walltime={job.time}')
        if job.isArray == True:
            scheduler_header.append(f'#PBS -J 1-{job.numJobs}:1')
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
    