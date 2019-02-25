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
curl localhost:9081/crawl.json -d '{"request":{"url":"http://dummy.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "ehazolve"}' | jq
  ```  
## CLI call
```
scrapy crawl ehazolve -a user="60987" -a password="XXXXXX"
```
## Docker start:
```
docker run -p 9080:9080 -tid -v /var/www/automation/londongdautomation/gdscraper:/scrapyrt/project scrapinghub/scrapyrt
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