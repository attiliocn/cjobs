def build_gaussian16_routine(scrdir, n_cores, job_input, container):
    g16_routine = []
    g16_routine.append(f'export GAUSS_SCRDIR=""${scrdir}"/src"')
    g16_routine.append(f'mkdir $GAUSS_SCRDIR')
    g16_routine.append(f'')
    g16_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    g16_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    g16_routine.append(f'export OMP_STACKSIZE=4G')
    g16_routine.append(f'ulimit -s unlimited')
    g16_routine.append(f'')
    g16_routine.append(
        f'''singularity run \\
    --bind="${scrdir}":"${scrdir}" \\
    {container} \\
    "${scrdir}" \\
    g16 "${job_input}" &'''
)
    g16_routine.append('wait')
    g16_routine.append(f'rm -r "$GAUSS_SCRDIR"')
    g16_routine.append('exit')
    return g16_routine

def build_orca5_routine(scrdir, n_cores, job_input, job_output, container):
    orca5_routine = []
    orca5_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    orca5_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    orca5_routine.append(f'export OMP_STACKSIZE=4G')
    orca5_routine.append(f'ulimit -s unlimited')
    orca5_routine.append(f'')
    orca5_routine.append(
        f'''singularity run \\
    --bind="${scrdir}":"${scrdir}" \\
    {container} \\
    "${scrdir}" \\
    "${job_input}" 1> "${job_output}".out 2> stderr.log &'''
)
    orca5_routine.append('wait')
    orca5_routine.append('exit')
    return orca5_routine

def build_xtb_routine(job:object):
    xtb_routine = []
    xtb_routine.extend(
        [
            '# <-- xtb execution routine',
            f'export MKL_NUM_THREADS={job.cpu}',
            f'export OMP_NUM_THREADS={job.cpu}',
            'export OMP_STACKSIZE=4G',
            'ulimit -s unlimited',
            '',
            'singularity run \\',
            '--bind="$PWD":"$PWD" \\',
            '"$ctPath" \\',
            '"$PWD" \\',
            f'xtb "$job" {job.options} &> xtb.output &',
            'wait',
            '# end of xtb execution routine -->'
        ]
    )
    return xtb_routine

def build_crest_routine(scrdir, n_cores, job_input, flags, container, standalone):
    crest_routine = []
    crest_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    crest_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    crest_routine.append(f'export OMP_STACKSIZE=4G')
    crest_routine.append(f'ulimit -s unlimited')
    crest_routine.append(f'')
    if standalone:
        flags = flags.split(' ')
        crest_routine.append(
            f'''singularity run \\
        --bind="${scrdir}":"${scrdir}" \\
        {container} \\
        "${scrdir}" \\
        crest {flags[0]} "${job_input}" {" ".join(flags[1:])} &> crest.output &'''
    )
    else:
        crest_routine.append(
            f'''singularity run \\
        --bind="${scrdir}":"${scrdir}" \\
        {container} \\
        "${scrdir}" \\
        crest "${job_input}" {flags} &> crest.output &'''
    )
    crest_routine.append('wait')
    crest_routine.append('exit')
    return crest_routine