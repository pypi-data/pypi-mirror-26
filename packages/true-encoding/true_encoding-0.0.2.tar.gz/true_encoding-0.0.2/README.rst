**crawl_requests**
==================

*Usage:*
--------
>>>import requests

>>>from true_encoding.true_encoding import Tcode ##

>>>res = requests.get('https://python.org')

>>>res.encoding = Tcode(res) ##

>>>content = res.text
