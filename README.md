# Farmer's Market

An extensible implementation of a checkout system that applies user defined discounts representing a Farmer's Market style business

## Getting Started

### Prerequisites

You will need the following to run the application

```
Docker version 18.03.1-ce
```

### Installing

1. Clone this repository
```bash
$ git clone https://github.com/rr1073/farmers_market_app.git
```
2. Run the following command in the project's root directory to build the docker image:
```bash
$ docker build --tag farmers_market .
```
3. Once built, execute this command to run the docker container as a daemon. </br></br>*Note:* Consider any other running docker services and ensure that port 8000 is available</br>
```bash
$ docker run --rm -p 8000:8000 -d farmers_market
```
4. Finally, open your preferred browser and view the running app on the following url
```
http://localhost:8000/
```
5. The user interface allows customers to add items to their cart.  Discounts will be applied when the item is added.

## Running the tests

You can run automated pytests that will test different product price outcomes

### Run all tests

```bash
$ docker exec -it <CONTAINER_NAME> pytest -v
```


## Helpful tips and commands

To find the "CONTAINER_NAME" value run the following command and look for the "farmers_market" IMAGE
```bash
$ docker ps

IMAGE                    NAMES
farmers_market           elegant_fermi
```

to stop the application run the following command
```bashInstalling
$ docker stop <CONTAINER_NAME>
```

to remove the app image
```bash
$ docker rmi -f farmers_market
```