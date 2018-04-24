#!/bin/sh
rm p1.json
rm p1_login.json
rm p1_nologin.json
rm p1_login_run2.json
python csrf/gen_config_nologin.py
scrapy crawl p1 -a config=config.json -o p1_nologin.json -L ERROR
python post_process.py p1_nologin.json

python csrf/gen_config_login.py
scrapy crawl p1 -a config=config.json -o p1_login.json -L ERROR
python post_process.py p1_login.json

python csrf/gen_config_login.py
scrapy crawl p1 -a config=config.json -o p1_login_run2.json -L ERROR
python post_process.py p1_login_run2.json

python csrf/csrf_scanner.py p1_nologin.json p1_login.json p1_login_run2.json
