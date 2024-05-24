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
    with open(f"{CJOBS_DIR}/extras/get_csv_element.sh") as f:
        jobfile.append(f.read())

    jobfile.append('')
    # write jobsteps to jobfile
    jobfile.append("{:#^40}".format('  JOB RUNTIME  '))
    jobfile.append('')

    jobfile.append('# trap signals if the job is either done or interrupted')
    jobfile.append('trap clean_job EXIT HUP INT TERM ERR')
    jobfile.append('')
        
    jobfile.append('# relevant directories')
    jobfile.append(f'localDir="{jobInfo.localDir}"')
    jobfile.append(f'scrDir="{jobInfo.scrDir}"')
    jobfile.append(f'usrScrDir="{jobInfo.usrScrDir}"')
    jobfile.append(f'exeDir="{jobInfo.exeDir}"')
    jobfile.append(f'ctDirRemote="{jobInfo.ctDir_remote}"')
    jobfile.append(f'ctDirLocal="{jobInfo.ctDir_local}"')
    jobfile.append(f'ct="{jobInfo.container}"')
    jobfile.append(f'ctPath="{jobInfo.ctDir_local}"/{jobInfo.container}')
    jobfile.append('')

    jobfile.append('# update containers')
    jobfile.append(f'echo "Requesting lock for synchronization using rclone."')
    jobfile.append(f'attempt_acquire_lock "$USER"_sync.lock "$scrDir" 3600')
    jobfile.append(f'create_directory_with_group_ownership "$ctDirLocal" {jobInfo.GID}')
    jobfile.append(f'fetch_containers_from_drive "$ctDirRemote" "$ctDirLocal"')
    jobfile.append(f'release_lock "$USER"_sync.lock "$scrDir"')
    jobfile.append('')

    jobfile.append('# load the singularity module')
    jobfile.append(f'module load singularity/{jobInfo.singularity_version}')
    jobfile.append('')

    jobfile.append('# job execution')
    jobfile.append('mkdir -p "$exeDir"')
    jobfile.append(f'rsync -avh "$localDir"/ "$exeDir"')
    jobfile.append('')
    jobfile.append(f'numjobs={jobInfo.numJobs}')
    jobfile.append(f'for job_number in $(seq 1 "$numjobs"); do')
    jobfile.append(util.indent(f'job={jobInfo.bashJobname}',4))
    jobfile.append(util.indent(f'basename="{jobInfo.bashBasename}"',4))
    jobfile.append(util.indent(f'jobDir="$exeDir"/"$basename"', 4))
    jobfile.append(util.indent('mkdir "$jobDir"', 4))
    jobfile.append(util.indent('cp "$job" "$jobDir"', 4))
    jobfile.append('')
    jobfile.append(util.indent('echo LOG: Current job: "$job"',4))
    jobfile.append(util.indent('echo LOG: Job basename: "$basename"',4))
    jobfile.append(util.indent('echo LOG: Running at: "$jobDir"',4))
    jobfile.append(util.indent('echo LOG: Singularity container path: "$ct_path"',4))
    jobfile.append('')
    jobfile.append(util.indent('cd "$jobDir"', 4))
    if jobInfo.software == 'gaussian':
        pass
    elif jobInfo.software == 'orca':
        pass
    elif jobInfo.software == 'xtb':
        job_routine = build_xtb_routine(jobInfo)
    elif jobInfo.software == 'crest':
        pass
    jobfile.extend([util.indent(s,4) for s in job_routine])
    jobfile.append(util.indent('cd "$exeDir"', 4))
    jobfile.append('')
    jobfile.append('done')    
    jobfile.append('')
    jobfile.append('exit')

    jobfile_content = "\n".join(jobfile)
    return jobfile_content


    
