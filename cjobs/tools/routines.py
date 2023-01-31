def build_gaussian16_routine(g16_scrdir, n_cores, job_input, container):
    g16_routine = []
    g16_routine.append(f'export $GAUSS_SCRDIR="{g16_scrdir}"')
    g16_routine.append(f'mkdir $GAUSS_SCRDIR')
    g16_routine.append(f'job_output=""$(echo "${job_input}" | rev | cut -f 2- -d \'.\' | rev)".log"')
    g16_routine.append(f'')
    g16_routine.append(f'export MKL_NUM_THREADS={n_cores}')
    g16_routine.append(f'export OMP_NUM_THREADS={n_cores}')
    g16_routine.append(f'export OMP_STACKSIZE=4G')
    g16_routine.append(f'ulimit -s unlimited')
    g16_routine.append(f'')
    g16_routine.append(f'singularity run {container} g16 < "${job_input}" > "$job_output"')
    return g16_routine