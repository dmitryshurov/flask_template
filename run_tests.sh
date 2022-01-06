PROJECT_NAME=${PWD##*/}
NETWORK_NAME=default

./init_db.sh --drop || exit 1
docker run -e TESTS_MASK=$1 --env-file .env --network=${PROJECT_NAME}_${NETWORK_NAME} --rm -it $(docker build -q -f build/services/tests/Dockerfile .)