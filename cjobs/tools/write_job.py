#!/usr/bin/env python3
import sys
import pathlib

from tools.scheduler_tools import build_scheduler_header
from tools.routines import build_gaussian16_routine, build_xtb_routine, build_crest_routine

def write_job(
    args, 
    scheduler, 
    containers_cloud_dir, 
    containers_local_dir,
    container,
    singularity_version,
    job_input,
    job_input_in_script,
    job_tag,
    job_name,
    job_local_dir,
    job_local_dir_in_script,
    job_scratch_dir,
    job_scratch_dir_in_script
):
    CJOBS_DIR = pathlib.Path(sys.argv[0]).parent

    # Write scheduler header to the job file
    jobfile = open(f'job_{job_tag}.sh', mode='w')
    jobfile.write('#!/bin/bash\n')
    scheduler_header = build_scheduler_header(scheduler=scheduler, job_name=job_tag, n_cores=args.cores, memory=args.memory_per_core, job_time=args.time)
    jobfile.write('\n'.join(scheduler_header)+'\n\n')

    # Write clean_job trap function to job file
    jobfile.write("{:#^80}".format('  CLEAN JOB  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/clean_job.sh") as f:
        jobfile.write(f.read()+'\n\n')

    # Write container settings to the job file
    jobfile.write("{:#^80}".format('  CONTAINER SETTINGS  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/get_containers.sh") as f:
        jobfile.write(f.read()+'\n')
    jobfile.write(f'get_containers {containers_cloud_dir} {containers_local_dir}\n')
    jobfile.write(f'module load singularity/{singularity_version}\n\n')

    # Write job directories to the job file
    jobfile.write("{:#^80}".format('  JOB INFORMATION  ')+'\n')
    jobfile.write(f'export job_input={job_input}\n')
    jobfile.write(f'export job_name={job_name}\n')
    jobfile.write(f'export {job_local_dir_in_script}="{job_local_dir}"\n')
    jobfile.write(f'export {job_scratch_dir_in_script}={job_scratch_dir}\n')
    jobfile.write(f'mkdir -p "${job_scratch_dir_in_script}"\n')
    jobfile.write('\n')
    jobfile.write(f'cp "${job_input_in_script}" "${job_scratch_dir_in_script}"\n')
    if args.send_files:
        jobfile.write(f'# send additional files to scratch dir\n')
        for file in args.send_files:
                jobfile.write(f'cp "${job_local_dir_in_script}"/{file} "${job_scratch_dir_in_script}"\n')
        jobfile.write('\n')
    jobfile.write(f'cd "${job_scratch_dir_in_script}"\n')
    jobfile.write('\n')

    # Write software settings to the job file
    jobfile.write("{:#^80}".format('  SOFTWARE SETTINGS  ')+'\n') 

    if args.subparser == 'gaussian':
        job_routine = build_gaussian16_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script, 
            container=f"{containers_local_dir}/{container}"
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'xtb':
        job_routine = build_xtb_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script, 
            flags=args.flags, 
            container=f"{containers_local_dir}/{container}"
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'crest':
        job_routine = build_crest_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script, 
            flags=args.flags, 
            container=f"{containers_local_dir}/{container}"
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    jobfile.close()
