export GAUSS_SCRDIR=""$job_scratch_dir"/scr"
mkdir $GAUSS_SCRDIR

export MKL_NUM_THREADS=8
export OMP_NUM_THREADS=8
export XTBHOME=""$HOME"/opt/chemsoft/xtb-6.5.1/"
source "$XTBHOME"/share/xtb/config_env.bash

sed -i "s#%chk=#%chk=$job_scratch_dir/#g" "$job_scratch_dir"/"$job_input"

"$GAUSS_EXEDIR"/g16 < "$job_scratch_dir"/"$job_input" > "$job_scratch_dir"/hydrogen.log &
wait
exit