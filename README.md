# A sample project

## Quickstart

### Prerequisites

* Linux
* Docker

### Run

1. Open a terminal and go to the repository root

2. Create an `.env` file from a template
```
cp .env_template .env
```

3. Generate a secret key and copy it to the `.env` file's SECRET_KEY variable
```
openssl rand -hex 32
```

4. Fill the `.env` file with your settings

5. Run the project
```
docker-compose up -d --build
```

### Test

After running the project as described above, just run all tests (it may take some time to build Docker image during the first run):

```
./run_tests.sh
```

To run a single test, specify a mask for a test name as an argument, e.g.:
```
./run_tests.sh 0001
```
