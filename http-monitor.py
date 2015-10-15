# -*- coding: utf-8 -*-

import requests, time, json, math, ConfigParser, logging
from dd import dd_api_access, post2datadog_metric, post2datadog_event
from get_urls_list import get_urls_list

# config.ini から設定ファイルの読み込み
c = ConfigParser.SafeConfigParser()
c.read("./config.ini")

# ログ出力の設定
log_fmt = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=log_fmt, level=logging.INFO)

# 指定した URL にアクセスしてレスポンスコードとレスポンスタイムを返す
def check_http_access(url):
    logging.info("=== elapsed.total_seconds() を利用して http レスポンスを確認")
    logging.info("=== %s にアクセス" % url)
    start = time.time()
    r = requests.request('GET', url)
    r.content
    roundtrip = time.time() - start
    # print roundtrip
    # return (round(r.elapsed.total_seconds(), 2), r.status_code)

    """
     - 小数点以下 2 桁でレスポンスタイムを返す
     - ステータスコードを返す
    """ 
    return (round(roundtrip, 2), r.status_code)

"""
 - access_list[0]
  - 0 ... Active
  - 1 ... InActive
 - access_list[1] = Datadog Title
 - access_list[2] = URL
 - access_list[3] = レスポンスタイムしきい値
"""
# def lambda_handler():
def lambda_handler(event, context):
    currenttime = time.time()
    urls_list = get_urls_list()
    for url_list in urls_list.split("\n"):
    	access_list = url_list.rstrip().split(",")
    	if str(access_list[0]) == '0':
    		res_time, res_code = check_http_access(access_list[2])
    		if res_code != 200:
    			post2datadog_event(c.get('datadog','title_prefix') + access_list[1], res_code, res_time, 'error')
    		elif res_code == 200 and res_time > float(access_list[3]):
    			post2datadog_event(c.get('datadog','title_prefix') + access_list[1], res_code, res_time, 'warning')

    		post2datadog_metric(c.get('datadog','title_prefix') + access_list[1], currenttime, res_time)

    #f = open('./url_list')
    #line = f.readline()
    #while line:
    #	access_list = line.rstrip().split(",")
    #	res_time, res_code = check_http_access(access_list[1])
    #	if res_code != 200:
    #		post2datadog_event('my.response.' + access_list[0]  + '.a', res_time, 'error')
    #	elif res_code == 200 and res_time > float(access_list[2]):
    #		post2datadog_event('my.response.' + access_list[0]  + '.a', res_time, 'warning')

    #	post2datadog_metric('my.response.' + access_list[0]  + '.a', currenttime, res_time)
    #    line = f.readline()
    #f.close

# lambda_handler()
