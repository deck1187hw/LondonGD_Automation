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
docker pull scrapinghub/scrapyrt
docker run -p 9080:9080 -tid --restart unless-stopped --name apigd -v /var/www/automation/londongdautomation/gdscraper:/scrapyrt/project scrapinghub/scrapyrt
```


## API Docs
### GET EHA Members
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://dummy.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "eha"}'
  ```  
  
  
## CLI call example
```
scrapy crawl eha -a user="60987" -a password="XXXXXX"
```