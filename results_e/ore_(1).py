import requests


req = requests.get("http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8080/princess.php", params={"target": "https://status.github.com/messages"}, headers={"Referrer": "http://google.com", "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"}, verify=False)


print(req.content)
