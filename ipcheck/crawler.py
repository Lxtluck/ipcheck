# !/usr/bin/env python
# *-* coding:utf-8 *-*

import scrapy
import sys
import json
import utils
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
key_word, ultimate_file, file_name = sys.argv[1], sys.argv[2], sys.argv[3]

print key_word, ultimate_file, file_name
try:
    with open('./temp_file/%s' % file_name, 'r') as f:
        url_list = json.loads(f.read())
except Exception as e:
    print e.message
    sys.exit(1)

def parse(self, response):
    content = response.text.decode('unicode-escape').encode('utf-8')
    if key_word in content:
        print content
        ip = response.url.split('=')[-1] + '\n'
        print ip
        with open('./%s' % ultimate_file, 'a+') as f:
            f.write(ip)
settings = get_project_settings()
runner = CrawlerRunner(settings)
configure_logging(settings)
num = 0
ip_list = list(utils.list_slice(url_list, 500))
for url in ip_list:
    num += 1
    Spider = type('Spider-%d' % num, (scrapy.Spider,), {'name': 'quo', 'parse': parse, 'start_urls': url})
    runner.crawl(Spider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
