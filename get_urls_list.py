# -*- coding: utf-8 -*-

from boto3 import Session
import ConfigParser, logging

# config.ini から設定ファイルの読み込み
c = ConfigParser.SafeConfigParser()
c.read("./config.ini")

# boto3 を利用して S3 上の URL リストを取得
def get_urls_list():
    logging.info("=== boto3 を利用して S3 上の URL リストを取得")
    s3 = Session().client('s3')
    response = s3.get_object(Bucket=c.get('s3','bucket_name'), Key=c.get('s3','urls_list'))
    body = response['Body'].read()
    # 内容をバルクで返す
    return body.strip()
