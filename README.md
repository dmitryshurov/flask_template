# A sample project

## Quickstart

### Prerequisities

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