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
    scheduler_header = build_scheduler_header(jobInfo)
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

    jobfile.append('# allocation details')
    jobfile.append(f'allocCPU={jobInfo.cpu}')
    jobfile.append(f'allocRAM={jobInfo.ram}')
    jobfile.append(f'g16GID={jobInfo.GID}')
    jobfile.append(f'')
        
    jobfile.append('# relevant directories')
    jobfile.append(f'localDir="{jobInfo.localDir}"')
    jobfile.append(f'scrDir="{jobInfo.scrDir}"')
    jobfile.append(f'usrScrDir="{jobInfo.usrScrDir}"')
    jobfile.append(f'exeDir="{jobInfo.exeDir}"')
    jobfile.append(f'ctDirRemote="{jobInfo.ctDirRemote}"')
    jobfile.append(f'ctDirLocal="{jobInfo.ctDirLocal}"')
    jobfile.append(f'ct="{jobInfo.containerFile}"')
    jobfile.append(f'ctPath="{jobInfo.ctDirLocal}"/{jobInfo.containerFile}')
    jobfile.append('')

    jobfile.append('# update containers')
    jobfile.append(f'echo "LOG: Requesting lock for synchronization using rclone."')
    jobfile.append(f'attempt_acquire_lock "$USER"_sync.lock "$scrDir" 3600')
    jobfile.append(f'create_directory_with_group_ownership "$ctDirLocal" "$g16GID"')
    jobfile.append(f'fetch_containers_from_drive "$ctDirRemote" "$ctDirLocal"')
    jobfile.append(f'release_lock "$USER"_sync.lock "$scrDir"')
    jobfile.append('')

    jobfile.append('# job execution')
    jobfile.append(f'echo "LOG: Creating execution directory"')
    jobfile.append('mkdir -p "$exeDir"')
    jobfile.append('cp "$localDir"/cjobs_*.sh "$localDir"/cjobs_joblist.csv "$exeDir"')
    jobfile.append('')

    # TODO: singularity loading should be explicitly configurated in the RC file
    if jobInfo.scheduler == 'pbs-pro':
        jobfile.append('# load the singularity module')
        jobfile.append('module load singularity')

    jobfile.append(f'numjobs={jobInfo.numJobs}')
    jobfile.append(f'echo "LOG: Running jobs"')
    if jobInfo.mode == 'massive':
        jobfile.append(f'for job_number in $(seq 1 "$numjobs"); do')
    else:
        jobfile.append('# NOTICE: This is not a massive job.')
        jobfile.append('#         The for loop will run only once.')
        jobfile.append(f'for job_number in {jobInfo.jobNumber}; do')        
    jobfile.append(util.indent(f'job={jobInfo.bashJobname}',4))
    jobfile.append(util.indent(f'basename="{jobInfo.bashBasename}"',4))
    jobfile.append(util.indent(f'jobDir="$exeDir"/"$basename"', 4))
    jobfile.append(util.indent('mkdir "$jobDir"', 4))
    jobfile.append(util.indent('cp "$localDir"/"$job" "$jobDir"', 4))
    if jobInfo.sendAdditionalFiles:
        for name,rename in jobInfo.additionalFiles:
            if rename:
                jobfile.append(util.indent(f'cp "$localDir"/{name} "$jobDir"/{rename} # additional file',4))
            else:
                jobfile.append(util.indent(f'cp "$localDir"/{name} "$jobDir" # additional file',4))
    jobfile.append('')
    jobfile.append(util.indent('echo LOG: Current job: "$job"',4))
    jobfile.append(util.indent('echo LOG: Job basename: "$basename"',4))
    jobfile.append(util.indent('echo LOG: Running at: "$jobDir"',4))
    jobfile.append(util.indent('echo LOG: Hostname: $(hostname)',4))
    jobfile.append(util.indent('echo LOG: Singularity container path: "$ctPath"',4))
    jobfile.append('')
    jobfile.append(util.indent('cd "$jobDir"', 4))
    if jobInfo.software == 'gaussian':
        job_routine = build_gaussian16_routine(jobInfo)
    elif jobInfo.software == 'orca':
        job_routine = build_orca5_routine(jobInfo)
    elif jobInfo.software == 'xtb':
        job_routine = build_xtb_routine(jobInfo)
    elif jobInfo.software == 'crest':
        job_routine = build_crest_routine(jobInfo)
    jobfile.extend([util.indent(s,4) for s in job_routine])
    jobfile.append(util.indent('cd "$exeDir"', 4))
    jobfile.append('done')    
    jobfile.append('')
    jobfile.append('exit')

    jobfile_content = "\n".join(jobfile)
    return jobfile_content


    
