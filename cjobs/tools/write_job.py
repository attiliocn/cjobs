#!/usr/bin/env python3
import sys
import pathlib

from tools.scheduler_tools import build_scheduler_header
from tools.routines import build_gaussian16_routine, build_orca5_routine, build_xtb_routine, build_crest_routine

def write_job(global_settings, job_settings, cli_args):
    
    CJOBS_DIR = pathlib.Path(sys.argv[0]).parent

    # open jobfile and write the bash shebang
    jobfile = open(f'job_{job_settings.jobID}.sh', mode='w')
    jobfile.write('#!/bin/bash\n')

    # write scheduler header to the job file
    scheduler_header = build_scheduler_header(
        scheduler=global_settings.scheduler, 
        job_name=job_settings.job_id, 
        n_cores=cli_args.cores, 
        memory=cli_args.memory_per_core, 
        job_time=cli_args.time,
        n_jobs=len(cli_args.job),
        job_array=cli_args.array
    )
    jobfile.write('\n'.join(scheduler_header)+'\n\n')

    # Write local variables definitions to job file
    jobfile.write("{:#^80}".format('  ENVIRONMENT  ')+'\n')
    jobfile.write('# job variables\n')
    jobfile.write(f'job_filename="{job_settings.job_filename}"\n')
    jobfile.write(f'job_basename="{job_settings.job_basename}"\n')
    jobfile.write('# local environment\n')
    jobfile.write(f'local_dir="{job_settings.local_dir}"\n')
    jobfile.write('# execution environment\n')
    jobfile.write(f'usr_scratch_dir="{job_settings.usr_scratch_dir}"\n')
    jobfile.write(f'execution_dir="{job_settings.execution_dir}"\n')
    jobfile.write('# containers\n')
    jobfile.write(f'ct_remote_dir="{job_settings.ct_remote_dir}"\n')
    jobfile.write(f'ct_local_dir="{job_settings.ct_local_dir}"\n')

    # Write clean_job trap function to job file
    jobfile.write("{:#^80}".format('  CLEAN JOB  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/clean_job.sh") as f:
        jobfile.write(f.read()+'\n\n')

    # Write container settings to the job file
    jobfile.write("{:#^80}".format('  CONTAINER SETTINGS  ')+'\n') 
    with open(f"{CJOBS_DIR}/extras/lock_utils.sh") as f:
        jobfile.write(f.read()+'\n')
    with open(f"{CJOBS_DIR}/extras/create_directory_with_group_ownership.sh") as f:
        jobfile.write(f.read()+'\n')
    with open(f"{CJOBS_DIR}/extras/fetch_containers_from_drive.sh") as f:
        jobfile.write(f.read()+'\n')
    
    jobfile.write(f'\n')
    jobfile.write(f'echo "Requesting lock for synchronization using rclone."\n')
    jobfile.write(f'attempt_acquire_lock "$USER"_sync.lock {scratch_dir} 3600\n')
    jobfile.write(f'create_directory_with_group_ownership {containers_local_dir} {shared_gid}\n')
    jobfile.write(f'fetch_containers_from_drive {containers_cloud_dir} {containers_local_dir}\n')
    jobfile.write(f'release_lock "$USER"_sync.lock {scratch_dir}\n\n')
    
    jobfile.write(f'module load singularity/{singularity_version}\n\n')

    




    ######
    jobfile.write("{:#^80}".format('  JOB INFORMATION  ')+'\n')
    jobfile.write(f'export {job_local_dir_in_script}="{job_local_dir}"\n')
    jobfile.write(f'cd "${job_local_dir_in_script}"\n')
    jobfile.write(f'export {job_scratch_dir_in_script}={job_scratch_dir}\n')
    jobfile.write(f'mkdir -p "${job_scratch_dir_in_script}"\n')
    jobfile.write('\n')
    if args.array:
         jobfile.write('# array control file\n')
         jobfile.write(f'cp "${job_local_dir_in_script}"/queue.conf "${job_scratch_dir_in_script}"\n')
         jobfile.write('\n')

    jobfile.write(f'export {job_input_in_script}={job_input}\n')
    jobfile.write(f'export {job_name_in_script}={job_name}\n')
    jobfile.write('\n')
    if args.send_files:
        jobfile.write(f'# send additional files to scratch dir\n')
        for file in args.send_files:
                jobfile.write(f'cp "${job_local_dir_in_script}"/{file} "${job_scratch_dir_in_script}"\n')      
    jobfile.write('\n')
    jobfile.write(f'cp "${job_input_in_script}" "${job_scratch_dir_in_script}"\n')
    jobfile.write(f'cd "${job_scratch_dir_in_script}"\n')
    jobfile.write('\n')
    jobfile.write(f'echo "Job Name: "${job_name_in_script}""\n')
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

    elif args.subparser == 'orca':
        job_routine = build_orca5_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script,
            job_output=job_name_in_script,
            container=f"{containers_local_dir}/{container}"
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'xtb':
        job_routine = build_xtb_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script, 
            flags=args.flags, 
            container=f"{containers_local_dir}/{container}",
            standalone=args.standalone
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    elif args.subparser == 'crest':
        job_routine = build_crest_routine(
            scrdir=job_scratch_dir_in_script, 
            n_cores=args.cores, 
            job_input=job_input_in_script, 
            flags=args.flags, 
            container=f"{containers_local_dir}/{container}",
            standalone=args.standalone
            )
        jobfile.write('\n'.join(job_routine)+'\n')

    jobfile.close()
