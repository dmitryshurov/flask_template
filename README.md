# A sample project

## Quickstart

### Prerequisites

* Linux
* Docker

*Note: depending on your Docker setup you may need to use `sudo` to run the commands below.*

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

5. Run the Docker stack
```
docker-compose up -d --build
```

6. Initialize the database
```
./init_db.sh
```


### Test

_**WARNING!** Do not run tests on a production server since it will completely destroy the database!_

After running the project as described above, just run all tests (it may take some time to build Docker image during the first run):

```
./run_tests.sh
```

To run a single test, specify a mask for a test name as an argument, e.g.:
```
./run_tests.sh 0001
```

### Re-create the database

If you wish to re-create the database (drop the old one and initialize a new one), run:
```
./init_db.sh --drop
```

Note that the above command is executed before running tests at the setup stage.