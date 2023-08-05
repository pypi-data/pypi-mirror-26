**crawl_requests**
=================
*1. Feactures:*
---------------
- *crawl_requests provides api of User-Agent_pool and proxy_pool.*
- *firstly, common requests; secondly, add user-agent requests; finally, add user-agent and proxy requests.*

*2. Usage:*
-----------
>>>from crawl_requests import req

>>>req.req_get(url='https://baidu.com',headers={},UA_pool=[],proxy_pool=[])

<Response [200]>


*3. Tips:*
----------
- *pip install crawl_requests*
- *Example: proxy_pool=[{'http': '62.81.245.12:3128'},{'https': '210.38.1.147:8080'}]*
