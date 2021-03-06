#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
import json
import requests

print('translate begin...')

# set baidu develop parameter
apiurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
appid = '20180816000194959'
secretKey = 'lWzwUiWmhRORknf68FCT'

# 翻译内容 源语言 翻译后的语言


def translateBaidu(content, fromLang='en', toLang='zh'):
    salt = str(random.randint(32768, 65536))
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode("utf-8")).hexdigest()

    try:
        paramas = {
            'appid': appid,
            'q': content,
            'from': fromLang,
            'to': toLang,
            'salt': salt,
            'sign': sign
        }
        response = requests.get(apiurl, paramas)
        jsonResponse = response.json()  # 获得返回的结果，结果为json格式
        dst = str(jsonResponse["trans_result"]
                  [0]["dst"])  # 取得翻译后的文本结果
        return dst
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(translateBaidu('Chunchun is lovely and so sweet heart. '))
    print(translateBaidu('于千万人之中遇见你所要遇见的人，于千万年之中，时间的无涯的荒野里，\
        没有早一步，也没有晚一步，刚巧牵起你的手', 'zh', 'en'))

print('ending...')

'''
# out put
Chunchun是如此可爱，如此甜蜜的心。
Meet the person you want to meet among millions of people.
In the endless wilderness of time,
in the course of millions of years, neither earlier nor later,
just take your hand.
'''
