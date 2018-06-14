# Farmer's Market

A modified checkout system used to determine special prices on several items for sale.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes (verified on linux env). 


### Prerequisites

You will need the following to be able to run the application

```
Docker
```

### Installing

1. clone repository
```bash
$ git clone https://github.com/rr1073/farmers_market_app.git
```
2. in master branch, run the following command in the root directory to build the docker image:
```bash
$ docker build --tag farmers_market .
```
3. once built, execute this command to run the docker container
```bash
$ docker run --rm -p 8000:8000 -d farmers_market
```
4. Finally, open your preferred browser and view the running app on the following url
```
http://localhost:8000/
```

## Running the tests

You can run automated pytests that will test different product price outcomes

### Run all tests

run test suite with the following command

```bash
$ docker exec -it <NAMES> pytest -v
```

## Helpful tips and commands

to find the "NAMES" value run the following command and look for the "farmers_market" IMAGE
```bash
$ docker ps

IMAGE                    NAMES
farmers_market           elegant_fermi
```

to stop the application run the following command
```bash
$ docker stop <NAMES>
```

to remove the app image
```bash
$ docker rmi -f farmers_market
```

