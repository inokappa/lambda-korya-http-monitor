# -*- coding: utf-8 -*-

import requests, time, json, math, ConfigParser, logging

# config.ini から設定ファイルの読み込み
c = ConfigParser.SafeConfigParser()
c.read("./config.ini")

# HTTP API を直接叩く
def dd_api_access(endpoint, data):
    url = "https://app.datadoghq.com/api/v1/" + endpoint + "?api_key=" + c.get('datadog','api_key')
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    #print json.dumps(data)

# Metric をポスト
def post2datadog_metric(metric, currenttime, point):
    logging.info("=== Datadog Metrics にポスト(point は小数点以下 2 桁で表現)")
    data = {'series': [{'metric': metric, 'points': [[currenttime, point]]}]}
    dd_api_access('series', data)

# Event をポスト
def post2datadog_event(title, res_code, res_time, level):
    logging.info("=== Datadog Event にポスト")
    text = 'Response code: ' + str(res_code) + '\n' +'Response time: ' + str(res_time) + ' sec'
    data = {'title': title, 'text': text, 'alert_type': level}
    dd_api_access('events', data)
