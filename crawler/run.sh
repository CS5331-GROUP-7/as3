#!/bin/sh
rm p1.json
python gen_config.py
scrapy crawl p1 -a config=config.json -o p1.json -L ERROR
python remove_dupes.py
