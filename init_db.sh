APP_NAME=__main__
CONTAINER_NAME=backend_1
PROJECT_NAME=${PWD##*/}
SOURCE_PATH=/src/source

DOCKER_COMMAND="docker exec -e PYTHONPATH=${SOURCE_PATH} -e FLASK_APP=${APP_NAME} -it ${PROJECT_NAME}_${CONTAINER_NAME} bash -c"
FLASK_COMMAND="cd ${SOURCE_PATH}/apps/backend && flask"

if [ "$1" = "--drop" ]; then
    ${DOCKER_COMMAND} "${FLASK_COMMAND} db_drop"
fi

${DOCKER_COMMAND} "${FLASK_COMMAND} db_create"