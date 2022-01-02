for source_file;
do 
    temp_file=${source_file}_envsubst
    envsubst < "${source_file}" > "{$temp_file}" && mv "{$temp_file}" "${source_file}"
done