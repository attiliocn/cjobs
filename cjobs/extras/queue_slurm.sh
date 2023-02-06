#!/bin/bash
shopt -s expand_aliases
source "$HOME"/.bashrc

jobs_queue='jobs_queue.txt'
jobs_sent='jobs_sent.txt'

if [[ ! -f "$jobs_queue" ]]; then
    ls job_*.sh | sort -V > "$jobs_queue"
fi

num_slots=50
num_jobs=$(wc -l <(squeue -u $USER | tail -n +2) | awk '{print $1}')
remaining_slots=$((num_slots-num_jobs))

cd "$(dirname "$0")" # crontab runs in $HOME as default, this line change this behavior

if [[ "$remaining_slots" -gt 0 ]]; then
    echo "You can submit "$remaining_slots" more jobs"
    head -n "$remaining_slots" $jobs_queue > to_send.acn
    while read -r line; do sbatch "$line"; done < to_send.acn
    cat to_send.acn >> $jobs_sent
    rm to_send.acn

    tail -n +"$((remaining_slots+1))" $jobs_queue > temp.acn
    mv temp.acn $jobs_queue
else
    echo "You cannot submit more jobs"
fi