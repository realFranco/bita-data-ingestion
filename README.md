# Bita data ingestion

Ingest data using an extensive data source and place it into a data repository.

The assessment is based on [Python](https://www.python.org), the solution has a naive
implementation and there is no exist a "strong" optimization implemented.

A constraint for this project expose that the implementation won't use `COPY` or any bulk import
mechanism that is native to [Postgres](https://www.postgresql.org).

## Index

- [TL;DR](#tldr)
- [Data flow](#flow)
- [Project structure](#project-structure)
- [Execution flow](#execution-flow)
- [Docker information](#docker-information)
- [Benchmark](#benchmark)
- [Notes](#notes)


## Tl;DR

If you want to start the project, go ahead and observe the [Execution flow](#execution-flow). My
recommendation is to read this `README.md` if it is your first time around here.

## Data flow

The data flow goes in this way:

- A clean of the data repository is conducted;
- Read of the entire file;
- Data connection (there is no existence of a connection pool);
- A data repository where to insert data will be allowed to store the rows collected;
    - A chunk is used in order to "limit" the quantity of rows to pass to the SQL transaction.

## Project structure

```bash
.docker/            --> Directory that contain the configuration used by "Docker".
    db-postgres/    --> Directory where to store the `.sql` files, currently a DML was created.
src/
    database/       --> Database connection configuration.
    ingest/         --> Directory to place the data ingestion responsibility.
    public/data/    --> Directory to place the public data to be used during the data ingestion.
    repository/     --> Directory to place the repository layer.
    store/          --> Directory to place the storage location responsibility.
```

## Execution flow

```bash
# Clone the project.
git clone x

# Copy and fill up the environment variables.
cp .docker/.env.dist .docker/.env

docker compose -f .docker/compose.yaml build

# Ref: https://docs.docker.com/engine/reference/commandline/compose_up/.
# Starts the containers in the background and leaves them running.
docker compose -f .docker/compose.yaml up --detach

# Or, run the `db` service only.
docker compose -f .docker/compose.yaml up db --detach

# Execution examples:

# Run the help argument.
docker compose -f .docker/compose.yaml run --rm cli python3 main.py --help

# Run the clean and insert data flows.
docker compose -f .docker/compose.yaml run --rm cli python3 main.py \
    --csv public/data/stockExample.csv

# Run this if your data input has many rows. Increment the chunk argument as you want.
# Keep in mind that there is not optimization and a well-resource approach is no implemented (yet).
docker compose -f .docker/compose.yaml run --rm cli python3 main.py \
    --chunk 250000 \
    --csv public/data/stockExample.csv

# Run only the data insertion flow.
docker compose -f .docker/compose.yaml run --rm cli python3 main.py \
    --clean false \
    --csv public/data/stockExample.csv \
    --insert true

# Run only the data insertion flow, chunk size is set to 1000 rows.
docker compose -f .docker/compose.yaml run --rm cli python3 main.py \
    --chunk 1000 \
    --clean false \
    --csv public/data/stockExample.csv \
    --insert true
```

## Docker information

As I am using [Docker](https://www.docker.com) for containerization purposes, during my development
flow I have this versions on my host machine.

```bash
# `docker --version`
Docker version 24.0.5, build ced0996

# `docker compose version`
Docker Compose version v2.20.2-desktop.1
```

## Benchmarks

The next comparison of chunks where called "benchmarks". The hardware use is the next one:

- CPU: M1 Pro;
- RAM: 16 GB;
- SSD as hard disk drive.

The Docker Desktop that I have been use has a limit of 5 Cores and 8 GB of RAM for the containers
that runs this tests:

| Rows      | Using DB index    | No DB index   |
|:---------:|:-----------------:|:-------------:|
| 100.000   |  34.030 secs.     | 0.8436 secs.  |
| 300.000   |  118.5797 secs.   | 4.7773 secs.  |
| 500.000   |  168.2027 secs.   | 6.8604 secs.  |
| 700.000   |  237.8263 secs.   | 14.3700 secs. |
| 1.000.000 |  186.8643 secs.   | 16.8604 secs. |
| 5.000.000 |  Unknown secs.    | Unknown secs. |

The time shown in the previous table is approximate, feel free to run it on your own hardware.

For the last insertion stage a few exceptions where experienced and no solution where implemented yet.

## Notes

- There is no:
    - A SQL injection verification, the `.csv` can damage the entire data infrastructure layer;
    - The typical "virtual environment" approach, please use the containerization technology in 
        order to avoid damage on your own host.
    - Unit testing implemented;
    - Code quality assurance as "cyclomatic complexity" or "static code analysis" where used
        so there is not warranty to follow all the [PEP](https://peps.python.org/pep-0000/)
        recommendations.
- I have in mind to create a few more static classes in order to follow the "Strategy" software
design pattern.
    - "Strategy Design Principle: Favor composition over inheritance".

🇩🇪 | 🇻🇪
