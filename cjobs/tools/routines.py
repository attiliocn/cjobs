def build_gaussian16_routine(job:object):
    g16_routine = []
    g16_routine.extend(
        [
            '# <-- gaussian execution routine',
            'export GAUSS_SCRDIR="$jobDir"/scr',
            'mkdir "$GAUSS_SCRDIR"',
            f'export MKL_NUM_THREADS={job.cpu}',
            f'export OMP_NUM_THREADS={job.cpu}',
            'export OMP_STACKSIZE=4G',
            'ulimit -s unlimited',
            '',
            'singularity run \\',
            '--bind="$PWD":"$PWD" \\',
            '"$ctPath" \\',
            '"$PWD" \\',
            'g16 "$job" &',
            'wait',
            'rm -r "$GAUSS_SCRDIR"',
            '# end of gaussian execution routine -->',
        ]
    )
    return g16_routine

def build_orca5_routine(job:object):
    orca5_routine = []
    orca5_routine.extend(
        [
            '# <-- orca execution routine',
            f'export MKL_NUM_THREADS={job.cpu}',
            f'export OMP_NUM_THREADS={job.cpu}',
            'export OMP_STACKSIZE=4G',
            'ulimit -s unlimited',
            '',
            'singularity run \\',
            '--bind="$PWD":"$PWD" \\',
            '"$ctPath" \\',
            '"$PWD" \\',
            '"$job" 1> "$basename".out 2> stderr.log &',
            'wait',
            '# end of orca execution routine -->',    
        ]
    )
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

def build_crest_routine(job:object):
    crest_routine = []
    crest_routine = []
    crest_routine.extend(
        [
            '# <-- crest execution routine',
            f'export MKL_NUM_THREADS={job.cpu}',
            f'export OMP_NUM_THREADS={job.cpu}',
            'export OMP_STACKSIZE=4G',
            'ulimit -s unlimited',
            'singularity run \\',
            '--bind="$PWD":"$PWD" \\',
            '"$ctPath" \\',
            '"$PWD" \\',
        ]
    )
    if job.standalone:
        options = job.options.split(' ')
        crest_routine.append(f'crest {options[0]} "$job" {" ".join(options[1:])} &> crest.output &')
    else:
        crest_routine.append(f'crest "$job" {job.options} &> crest.output &')
    crest_routine.extend(
        [
            'wait',
            '# end of xtb execution routine -->'
        ]
    )
    return crest_routine