project_name=${PWD##*/}

SOURCE_PATH=/src/source
DOCKER_COMMAND="docker exec -e PYTHONPATH=${SOURCE_PATH} -e FLASK_APP=__main__ -it ${project_name}_backend_1 bash -c"
FLASK_COMMAND="cd ${SOURCE_PATH}/apps/backend && flask"

if [ "$1" = "--drop" ]; then
    ${DOCKER_COMMAND} "${FLASK_COMMAND} db_drop"
fi

${DOCKER_COMMAND} "${FLASK_COMMAND} db_create"