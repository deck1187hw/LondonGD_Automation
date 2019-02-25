# London GD Automation

[![N|Solid](https://londongdhandball.co.uk/templates/londongd2015/img/logo.png)](https://londongdhandball.co.uk)

Automation tools built in Python Scrapy to automate common tasks for London GD Handball club website


# Basic Instruction to run a spider 


```sh
$ git clone https://github.com/deck1187hw/londongdautomation.git
$ cd londongd
$ scrapy crawl classifications

Import kempa articles
$ scrapy crawl kempa -a filename=kempa-cats.txt 

Import kempa categories
$ scrapy crawl kempacat -a filename=kempa-cats.txt
```

# Run Scrapyrt to run API queries to scrapy
```
$ docker pull scrapinghub/scrapyrt
$ docker run -p 9080:9080 -tid -v /var/www/automation/londongdautomation/scrapy_app:/scrapyrt/project scrapinghub/scrapyrt
```


## API META 
```
curl localhost:9081/crawl.json -d '{"request":{"url":"http://example.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "ehazolve"}' | jq
  ```  
## CLI call
```
scrapy crawl ehazolve -a user="60987" -a password="king&country!"
```
## Docker start:
```
docker run -p 9080:9080 -tid -v /var/www/automation/londongdautomation/matchreport:/scrapyrt/project scrapinghub/scrapyrt
```
## With autorestart (localhost)
```
docker run -p 9080:9080 -tid --restart unless-stopped -v /var/www/automation/londongdautomation/matchreport:/scrapyrt/project scrapinghub/scrapyrt
```
## Run query (localhost)
```
curl localhost:9080/crawl.json -d '{"request":{"url":"http://example.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "ehazolve"}'
  ```  
## Run query (ip)
```
curl 138.68.175.93:9080/crawl.json -d '{"request":{"url":"http://example.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "ehazolve"}'
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
If Docker goes down:
```
docker start mongo_instance_001
```
Access the Mongo Shell
```
docker exec -it mongo_instance_001 /bin/bash
```

### Backup MongoDB
```
docker run -d -v /var/www/gd_backups/mongodb:/backup -e 'CRON_SCHEDULE=0 1 * * *' --link mongo_instance_001:mongo --name docker_backup istepanov/mongodump
```
