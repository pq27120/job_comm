import gzip
from http import cookiejar
from lib2to3.pgen2 import parse
from urllib import request

__author__ = 'pq'

cj = cookiejar.LWPCookieJar()
cookies = request.HTTPCookieProcessor(cj)
opener  = request.build_opener(cookies)

#默认协议头
DefaultHeaders = {
            "Accept":"*/*",
            "User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)",
            "Accept-Language":"zh-cn",
            "Accept-Encoding":"gzip;deflate",
            "Connection":"keep-alive",
            "Referer":"http://qzone.qq.com"
}

#GET访问
def Http(url,charset="utf-8",headers=DefaultHeaders):
    rr = request.Request(url=url, headers=headers)
    with opener.open(rr) as fp:
        if fp.info().get("Content-Encoding") == 'gzip':
            f = gzip.decompress(fp.read())
            res = f.decode(charset,'ignore')
        else:
            res = fp.read().decode(charset,'ignore')
    return res

#POST访问
def Post(url,postdata,charset="utf-8",headers=DefaultHeaders):
    if postdata:
        postdata = parse.urlencode(postdata).encode("utf-8")
    rr = request.Request(url=url,headers=headers,data=postdata)
    with opener.open(rr) as fp:
        if fp.info().get("Content-Encoding") == "gzip":
            f = gzip.decompress(fp.read())
            res = f.decode(charset)
        else:
            res = fp.read().decode(charset)
    return res