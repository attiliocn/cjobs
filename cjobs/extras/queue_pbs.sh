#!/bin/bash
shopt -s expand_aliases
source "$HOME"/.bashrc

cd "$(dirname "$0")" # crontab runs in $HOME as default

alias qstat='/opt/pbs/default/bin/qstat'
alias qsub='/opt/pbs/default/bin/qsub'

jobs_queue='jobs_queue.txt'
jobs_sent='jobs_sent.txt'

if [[ ! -f "$jobs_queue" ]]; then
    ls job_*.sh | sort -V > "$jobs_queue"
fi

num_jobs=$(wc -l <(qstat -u $USER | grep '.service') | awk '{print $1}')
remaining_slots=$((20-num_jobs))

if [[ "$remaining_slots" -gt 0 ]]; then
    echo "You can submit "$remaining_slots" more jobs"
    head -n "$remaining_slots" $jobs_queue > to_send.acn
    while read -r line; do qsub "$line"; done < to_send.acn
    cat to_send.acn >> $jobs_sent
    rm to_send.acn

    tail -n +"$((remaining_slots+1))" $jobs_queue > temp.acn
    mv temp.acn $jobs_queue
else
    echo "You cannot submit more jobs"
fi