project_name=${PWD##*/}

./init_db.sh --drop
docker run -e TESTS_MASK=$1 --env-file .env --network=${project_name}_default --rm -it $(docker build -q -f build/services/tests/Dockerfile .)