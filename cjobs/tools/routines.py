def build_gaussian16_routine(scrdir, n_cores, job_input, container):
    g16_routine = []
    g16_routine.append(f'export $GAUSS_SCRDIR=""${scrdir}"/src"')
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
    g16_routine.append('exit')
    return g16_routine

def build_xtb_routine(scrdir, n_cores, job_input, flags, container):
    xtb_routine = []
    xtb_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    xtb_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    xtb_routine.append(f'export OMP_STACKSIZE=4G')
    xtb_routine.append(f'ulimit -s unlimited')
    xtb_routine.append(f'')
    xtb_routine.append(
        f'''singularity run \\
    --bind="${scrdir}":"${scrdir}" \\
    {container} \\
    "${scrdir}" \\
    xtb "${job_input}" {" ".join(flags)} &> xtb.output'''
)
    return xtb_routine