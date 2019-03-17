# London GD Automation

[![N|Solid](https://londongdhandball.co.uk/templates/londongd2015/img/logo.png)](https://londongdhandball.co.uk)

Automation tools built in Python Scrapy to automate common tasks for London GD Handball club website. With API access (POST)

# Run Scrapyrt to run API queries to scrapy
```
docker pull scrapinghub/scrapyrt
docker stop apigd; docker rm apigd; docker run -p 9080:9080 -tid --restart unless-stopped --name apigd -v /var/www/automation/londongdautomation/gdscraper:/scrapyrt/project scrapinghub/scrapyrt
```


## API Docs

### GET EHA Fixtures (HTML table)
#### Get PHL Women
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://www.englandhandball.com/league/premier-handball-league", "meta": {"type":"women", "teamId": "5c6b312a6b1a993e85c466ec" }}, "spider_name": "ehafixtures"}'
  ```
  
#### Get PHL Men
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://www.englandhandball.com/league/premier-handball-league", "meta": {"type":"men", "teamId": "5c6b2fe800443f3db1b4e73c" }}, "spider_name": "ehafixtures"}'
  ```  



### GET EHA Members
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"http://notneeded.com", "meta": {"user":"60987", "password": "xxxx" }}, "spider_name": "eha"}'
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


### GET SportEasy Trainings Matches
```
curl https://automation.londongdhandball.co.uk/crawl.json -d '{"request":{"url":"https://www.sporteasy.net/en/login/"}, "spider_name": "sporteasytrainings"}'
  ```



## CLI call example
### Get all EHA users
```
scrapy crawl eha -a user="60987" -a password="XXXXXX"
```
### Get all fixtures
```
scrapy crawl ehafixtures
```

