# London GD Automation

[![N|Solid](https://londongdhandball.co.uk/templates/londongd2015/img/logo.png)](https://londongdhandball.co.uk)

Automation tools built in Python Scrapy to automate common tasks for London GD Handball club website


# Basic Instruction to run a spider


```sh
$ git clone https://github.com/deck1187hw/londongdautomation.git
$ cd londongd
$ scrapy crawl classifications
```


# Install and Run database (Docker)
```
$ cd mongodb/
```
### Building the MongoDB Docker image
With our Dockerfile, we can now build the MongoDB image using Docker. Unless experimenting, it is always a good practice to tag Docker images by passing the --tag option to docker build command.

```
docker build --tag my/database .
```
Once this command is issued, Docker will go through the Dockerfile and build the image. The final image will be tagged my/database
### Using the MongoDB image
Using the MongoDB image we created, we can run one or more MongoDB instances as daemon process(es).
```
# Dockerized MongoDB, lean and mean!
$ docker run -p 27017:27017 --name mongo_instance_001 -d my/database --smallfiles

# Checking out the logs of a MongoDB container
$ docker logs mongo_instance_001

# Playing with MongoDB
# Port you get from `docker ps`
$ mongo --port 27017

# If using docker-machine
# Usage: mongo --port <port you get from `docker ps`>  --host <ip address from `docker-machine ip VM_NAME`>
$ mongo --port 27017 --host 192.168.59.103
```