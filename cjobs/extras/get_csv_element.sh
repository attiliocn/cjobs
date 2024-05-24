function get_csv_element() {
    local csv_file=$1
    local row=$2
    local column=$3

    sed "${row}q;d" $csv_file | awk -F ',' -v col="$column" '{print $col}'
}