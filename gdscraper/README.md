# London GD Automation

[![N|Solid](https://londongdhandball.co.uk/templates/londongd2015/img/logo.png)](https://londongdhandball.co.uk)

Automation tools built in Python Scrapy to automate common tasks for London GD Handball club website. With API access (POST)

# Run Scrapyrt to run API queries to scrapy
```
docker pull scrapinghub/scrapyrt
docker stop apigd; docker rm apigd; docker run -p 9080:9080 -tid --restart unless-stopped --name apigd -v /var/www/automation/londongdautomation/gdscraper:/scrapyrt/project scrapinghub/scrapyrt
```


## API Docs
### GET EHA Members
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://dummy.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "eha"}'
  ```


### GET EHA Matches
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://www.englandhandball.com/league/premier-handball-league"}, "spider_name": "ehamatches"}'
  ```
| Urls allowed        |
| ------------- |
| http://www.englandhandball.com/league/premier-handball-league |
| http://www.englandhandball.com/regional-development-league/regional-league-south-east-tier-1-1/women |
| http://www.englandhandball.com/regional-development-league/regional-league-south-east-tier-1/men |
| http://www.englandhandball.com/regional-development-league/regional-league-south-east-a/men |



## CLI call example
```
scrapy crawl eha -a user="60987" -a password="XXXXXX"
```


