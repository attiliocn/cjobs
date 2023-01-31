#!/usr/bin/env python3

def write_cluster_script():
    job_file = open('job.txt', mode='w')

    job_file.write("{:#^80}".format('   CLEAN JOB   ')+'\n') 
    with open(f"{CJOBS_DIR}/tools/clean_job.sh") as f:
        job_file.write(f.read()+'\n')

    job_file.write(
        "{:#^80}".format('   JOB VARIABLES   ')+'\n'
        f'job_input="{JOB_BASENAME}.{JOB_INPUT_EXTENSION}"\n'
        f'job_submit_dir="{JOB_SUBMIT_DIR}"\n'
        '\n'
        f'job_local_dir=""$job_submit_dir"/{JOB_BASENAME}"\n'
        'mkdir -p $job_local_dir\n'
        '\n'
        f'job_scratch_dir="{JOB_SCRDIR}"\n'
        'mkdir -p $job_scratch_dir\n'
        '\n'
        #f'cp "$job_submit_dir"/"$job_input" "$job_local_dir"\n'
        f'cp "$job_submit_dir"/"$job_input" "$job_scratch_dir"\n'
        f'cd $job_scratch_dir\n'
        '\n'
    )
    job_file.close()
