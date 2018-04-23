import json
import os

crawled_items = json.load(open('p1.json'))

if len(crawled_items)>0:
    crawled_items_str = []
    for c in crawled_items:
        crawled_items_str.append(json.dumps(c))

    nodupes = list(set(crawled_items_str))
    print str(len(crawled_items_str)-len(nodupes)) + ' duplicates removed'
    with open('p1.json', 'w') as outfile:
        outfile.write('[\n')
        for i in xrange(len(nodupes)):
            line = nodupes[i]
            if i==len(nodupes)-1:outfile.write(line+'\n')
            else:outfile.write(line+',\n')
        outfile.write(']\n')

