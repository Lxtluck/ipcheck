# !/usr/bin/env python
# *-* coding:utf-8 *-*
import subprocess
import json
import sys
import utils
import os
import multiprocessing

key_word = raw_input('输入要查找的国家或者省份或者城市:')
resource_file = raw_input('把源文件放当前目录,文件名字(加文件扩展名e.g.txt):')
ultimate_file = raw_input('最终生成文件放在当前目录,文件名字(加文件扩展名e.g.txt):')
if not os.path.isfile(resource_file):
    raise Exception('输入得文件不存在')
if os.path.isfile(ultimate_file):
    raise Exception('该文件名已经存在,请输入新的文件名')
if resource_file.split('.')[-1] != 'txt' and ultimate_file.split('.')[-1] != 'txt':
    raise Exception('源文件和最终生成文件扩展名必须是txt结尾')

os.system('touch %s' % ultimate_file)
target_url = 'http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip=%s'
child_process_list = []
if os.path.isdir('temp_file'):
    os.system('rm %s' % ultimate_file)
    raise Exception('先把临时文件夹删了, 再进行ip查找')
os.mkdir('temp_file')

try:
    with open('./%s' % resource_file, 'r') as f:
        temp_str = f.readlines()[0]
        f.seek(0)
        if isinstance(temp_str, unicode):
            temp_str = temp_str.encode('utf-8')
            if len(temp_str) <= 16:
                temp_readlines = map(lambda line: line.encode('utf-8'), f.readlines())             
                url_list = [target_url % url.strip('\n') for url in temp_readlines]
            else:
                 raise Exception('file format may have problem')
        elif isinstance(temp_str, str) and len(temp_str) <= 16:
            url_list = [target_url % url.strip('\n') for url in f.readlines()]
        else:
            raise Exception('file format may have problem')
                    
except Exception as e:
    print e.message
    sys.exit(1)


if multiprocessing.cpu_count():
    #暂定进程数是cpu的5倍
    process_num = multiprocessing.cpu_count() * 5
    total_ip = utils.div_list(url_list, process_num)
    for count in xrange(process_num):
        temp_name = 'ip_%d.txt' % count
        with open('./temp_file/%s' % temp_name, 'w') as f:
            f.write(json.dumps(total_ip[count]))
        params_list = ['python', './crawler.py', key_word, ultimate_file, temp_name]
        p = subprocess.Popen(params_list)
        child_process_list.append(p)

for process in child_process_list:
    print '进程%d'%process.pid
    process.wait()

os.popen('rm -rf temp_file')    
