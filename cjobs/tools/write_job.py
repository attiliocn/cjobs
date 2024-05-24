#!/usr/bin/env python3
import sys
import pathlib

from tools.scheduler_tools import build_scheduler_header
from tools.routines import build_gaussian16_routine, build_orca5_routine, build_xtb_routine, build_crest_routine
import tools.util as util

def get_jobfile(jobInfo:object):
    CJOBS_DIR = pathlib.Path(sys.argv[0]).parent
    jobfile = []
    jobfile.append('#!/bin/bash')

    # write scheduler header to the job file
    scheduler_header = build_scheduler_header(
        scheduler=jobInfo.scheduler, 
        job_name=jobInfo.cjobsID, 
        n_cores=jobInfo.cpu, 
        memory=jobInfo.ram, 
        job_time=jobInfo.time,
        n_jobs=jobInfo.numJobs,
        job_array=jobInfo.isArray
    )
    jobfile.append('')

    jobfile.append("{:#^40}".format('  SCHEDULER  '))
    jobfile.append('')

    jobfile.extend(scheduler_header)
    jobfile.append('')

    # append local variables definitions to job file
    jobfile.append("{:#^40}".format('  ENVIRONMENT  '))
    jobfile.append('')
        
    jobfile.append('# local environment')
    jobfile.append(f'localDir="{jobInfo.localDir}"')
    jobfile.append('')

    jobfile.append('# execution environment')
    jobfile.append(f'scrDir="{jobInfo.scrDir}"')
    jobfile.append(f'exeDir="{jobInfo.exeDir}"')
    jobfile.append('')

    jobfile.append('# containers')
    jobfile.append(f'ctDir_remote="{jobInfo.ctDir_remote}"')
    jobfile.append(f'ctDir_local="{jobInfo.ctDir_local}"')
    jobfile.append(f'ct="{jobInfo.container}"')
    jobfile.append('')

    jobfile.append('# job variables')
    if jobInfo.isArray:
        jobfile.append(f'jobs={jobInfo.schedulerID}')
        jobfile.append(f'basenames="{jobInfo.basenames}"')
    else:
        jobfile.append(f'jobs=({util.py_array_to_bash(jobInfo.filenames)})')
        jobfile.append(f'basenames=({util.py_array_to_bash(jobInfo.basenames)})')
    jobfile.append('')
   
    # write function definitions to jobfile
    jobfile.append("{:#^40}".format('  FUNCTIONS  '))
    jobfile.append('') 
    with open(f"{CJOBS_DIR}/extras/clean_job.sh") as f:
        jobfile.append(f.read())
    with open(f"{CJOBS_DIR}/extras/lock_utils.sh") as f:
        jobfile.append(f.read())
    with open(f"{CJOBS_DIR}/extras/create_directory_with_group_ownership.sh") as f:
        jobfile.append(f.read())
    with open(f"{CJOBS_DIR}/extras/fetch_containers_from_drive.sh") as f:
        jobfile.append(f.read())

    jobfile.append('')
    # write jobsteps to jobfile
    jobfile.append("{:#^40}".format('  JOB RUNTIME  '))
    jobfile.append('')

    jobfile.append('# trap signals if the job is either done or interrupted')
    jobfile.append('trap clean_job EXIT HUP INT TERM ERR')
    jobfile.append('')

    jobfile.append('# update the local containers as needed')
    jobfile.append(f'echo "Requesting lock for synchronization using rclone."')
    jobfile.append(f'attempt_acquire_lock "$USER"_sync.lock {jobInfo.ctDir_local} 3600')
    jobfile.append(f'create_directory_with_group_ownership {jobInfo.ctDir_local} {jobInfo.GID}')
    jobfile.append(f'fetch_containers_from_drive {jobInfo.ctDir_remote} {jobInfo.ctDir_local}')
    jobfile.append(f'release_lock "$USER"_sync.lock {jobInfo.ctDir_local}')
    jobfile.append('')

    jobfile.append('# load the singularity module')
    jobfile.append(f'module load singularity/{jobInfo.singularity_version}')
    jobfile.append('')

    jobfile.append('# job execution')
    jobfile.append(f'mkdir -p "$exeDir"')
    jobfile.append(f'rsync -avh "$localDir" "$exeDir"')
    jobfile.append('')

    # if jobInfo.software == 'gaussian':
    #     job_routine = build_gaussian16_routine(
    #         scrdir='scr', 
    #         n_cores=jobInfo.ram, 
    #         job_input='input', 
    #         container=f"{containers_local_dir}/{container}"
    #         )
    #     jobfile.write('\n'.join(job_routine)+'\n')

    # elif jobInfo.software == 'orca':
    #     job_routine = build_orca5_routine(
    #         scrdir=job_scratch_dir_in_script, 
    #         n_cores=args.cores, 
    #         job_input=job_input_in_script,
    #         job_output=job_name_in_script,
    #         container=f"{containers_local_dir}/{container}"
    #         )
    #     jobfile.write('\n'.join(job_routine)+'\n')

    if jobInfo.software == 'xtb':
        job_routine = build_xtb_routine(jobInfo)
        

    # elif jobInfo.software == 'crest':
    #     job_routine = build_crest_routine(
    #         scrdir=job_scratch_dir_in_script, 
    #         n_cores=args.cores, 
    #         job_input=job_input_in_script, 
    #         flags=args.flags, 
    #         container=f"{containers_local_dir}/{container}",
    #         standalone=args.standalone
    #         )
    jobfile.extend(job_routine)





    jobfile.append('')
    jobfile.append('exit')
    jobfile_content = "\n".join(jobfile)
    return jobfile_content




    # jobfile.write(f'export {job_input_in_script}={job_input}\n')
    # jobfile.write(f'export {job_name_in_script}={job_name}\n')
    # jobfile.write('\n')
    # if args.send_files:
    #     jobfile.write(f'# send additional files to scratch dir\n')
    #     for file in args.send_files:
    #             jobfile.write(f'cp "${job_local_dir_in_script}"/{file} "${job_scratch_dir_in_script}"\n')      
    # jobfile.write('\n')
    # jobfile.write(f'cp "${job_input_in_script}" "${job_scratch_dir_in_script}"\n')
    # jobfile.write(f'cd "${job_scratch_dir_in_script}"\n')
    # jobfile.write('\n')
    # jobfile.write(f'echo "Job Name: "${job_name_in_script}""\n')
    # jobfile.write('\n')

    # # Write software settings to the job file
    # jobfile.write("{:#^80}".format('  SOFTWARE SETTINGS  ')+'\n') 



    
