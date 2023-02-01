#!/usr/bin/env python3

from tools.scheduler_tools import build_scheduler_header
from tools.routines import build_gaussian16_routine, build_xtb_routine, build_crest_routine

def write_job():
    # Write scheduler header to the job file
    jobfile = open(f'job_{job_tag}.sh', mode='w')
    jobfile.write('#!/bin/bash\n')
    scheduler_header = build_scheduler_header(scheduler=QUEUE_SYSTEM, job_name=job_tag, n_jobs=n_jobs, n_cores=args.cores, memory=args.memory_per_core, job_time=walltime)
    jobfile.write('\n'.join(scheduler_header)+'\n\n')

    # Write clean_job trap function to job file
    jobfile.write("{:#^80}".format('  CLEAN JOB  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/clean_job.sh") as f:
        jobfile.write(f.read()+'\n\n')

    # Write container settings to the job file
    jobfile.write("{:#^80}".format('  CONTAINER SETTINGS  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/get_containers.sh") as f:
        jobfile.write(f.read()+'\n')
    jobfile.write(f'get_containers {CONTAINERS_CLOUD_DIR} {CONTAINERS_LOCAL_DIR} \n\n')

    # Write job directories to the job file
    jobfile.write("{:#^80}".format('  JOB INFORMATION  ')+'\n')
    jobfile.write(f'export job_input={job_input}\n')
    jobfile.write(f'export job_name={job_name}\n')
    jobfile.write(f'export {job_local_dir_in_script}="{job_local_dir}"\n')
    jobfile.write(f'export {job_scratch_dir_in_script}={job_scratch_dir}\n')
    jobfile.write(f'mkdir "${job_scratch_dir_in_script}"\n')
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
        job_routine = build_gaussian16_routine(scrdir=job_scratch_dir_in_script, n_cores=args.cores, job_input=job_input_in_script, container=f"{CONTAINERS_LOCAL_DIR}/{containers_data[args.container]['file']}")
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'xtb':
        job_routine = build_xtb_routine(scrdir=job_scratch_dir_in_script, n_cores=args.cores, job_input=job_input_in_script, flags=args.flags, container=f"{CONTAINERS_LOCAL_DIR}/{containers_data[args.container]['file']}")
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'crest':
        job_routine = build_crest_routine(scrdir=job_scratch_dir_in_script, n_cores=args.cores, job_input=job_input_in_script, flags=args.flags, container=f"{CONTAINERS_LOCAL_DIR}/{containers_data[args.container]['file']}")
        jobfile.write('\n'.join(job_routine)+'\n')

    jobfile.close()
