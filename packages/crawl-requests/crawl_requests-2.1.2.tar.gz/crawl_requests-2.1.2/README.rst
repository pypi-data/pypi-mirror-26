**crawl_requests**
==================
*1. Feactures:*
---------------
- *crawl_requests(like requests) can update ua and proxy automatically.*

*2. Usage:*
-----------
>>>from crawl_requests import req2

>>>rq2 = req2.Req2()

>>>rq2.keep_req(method='get',url='https://www.python.org')

<Response [200]>

*3. Tips:*
----------
- *pip install crawl_requests*
- *req2 updates ua and proxy automatically.*
- *rq2 need about 10 minutes to load and test proxy to be used.*