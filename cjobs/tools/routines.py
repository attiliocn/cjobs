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

def build_xtb_routine(scrdir, n_cores, job_input, flags, container, standalone=False):
    xtb_routine = []
    xtb_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    xtb_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    xtb_routine.append(f'export OMP_STACKSIZE=4G')
    xtb_routine.append(f'ulimit -s unlimited')
    xtb_routine.append(f'')
    if standalone:
        flags = flags.split(' ')
        xtb_routine.append(
            f'''singularity run \\
        --bind="${scrdir}":"${scrdir}" \\
        {container} \\
        "${scrdir}" \\
        xtb {flags[0]} "${job_input}" {" ".join(flags[1:])} &> xtb.output &'''
    )
    else:
        xtb_routine.append(
            f'''singularity run \\
        --bind="${scrdir}":"${scrdir}" \\
        {container} \\
        "${scrdir}" \\
        xtb "${job_input}" {flags} &> xtb.output &'''
    )
    xtb_routine.append('wait')
    xtb_routine.append('exit')
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
        crest {flags[0]} "${job_input}" {" ".join(flags[1:])} &> xtb.output &'''
    )
    else:
        crest_routine.append(
            f'''singularity run \\
        --bind="${scrdir}":"${scrdir}" \\
        {container} \\
        "${scrdir}" \\
        crest "${job_input}" {flags} &> xtb.output &'''
    )
    crest_routine.append('wait')
    crest_routine.append('exit')
    return crest_routine