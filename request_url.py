"""
利用https://www.xicidaili.com/nn/页面提供的http代理访问网站
BeautifulSoup 安装 https://www.cnblogs.com/sunnywss/p/6640154.html
安装lxml解析库：pip install --user lxml
程序参考：
https://blog.csdn.net/Lammonpeter/article/details/52917264
https://www.cnblogs.com/xinyangsdut/p/7625714.html
"""
import requests
from bs4 import BeautifulSoup
import random

# 禁止warning，不加会有https安全提示
requests.packages.urllib3.disable_warnings()

cookie = 'SUB=_2AkMsth9Mf8NxqwJRmP4Tz2jlbYt1yQDEieKa6u6XJRMxHRl-yT83qnwltRB6BzYxowKwERot0p6914E3L2RPl6x3K7XV; ' \
         'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9Wh4kL089PFpmGGcbvae8BUA; YF-V5-G0=aac25801fada32565f5c5e59c7bd227b; ' \
         'YF-Page-G0=b1e3c8e8ad37eca95b65a6759b3fc219|1554081013|1554081001; Ugrow-G0=8751d9166f7676afdce9885c6d31cd61 '


# 解析html得到代理ip
def get_ip_list(content):
    soup = BeautifulSoup(content, 'lxml')
    html_ips = soup.find_all('tr')
    ip_list = []
    for index in range(1, len(html_ips)):
        html_ip_info = html_ips[index]
        tds = html_ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


# 从ip_list中随机选一个ip构造成为代理
def get_random_ip(ip_list):
    proxy_ip = random.choice(ip_list)
    proxies = {'http': 'http://' + proxy_ip}
    return proxies


# 访问url得到html，返回html中的ip列表
def get_proxy(ip_list, count):
    for i in range(count):
        base_url = 'https://www.xicidaili.com/nn/'
        # 网站访问规则是 /nn/，/nn/2，/nn/3...
        if i > 1:
            base_url = base_url + str(i)
        content = get_url(base_url, None)
        ip_list.extend(get_ip_list(content))
    return


# 访问https网页
def get_url(url, proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/31.0.1650.48',
        'Cookie':cookie}
    response = requests.get(url, headers=headers,
                            verify=False, proxies=proxy)
    print('code:%s, proxy:%s' % (response.status_code, proxy))
    return response.content


if __name__ == '__main__':
    comment = open('comment_cache', 'wb+')
    for i in range(80000, 80001):
        base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=3424883176420210&page=' \
                   + str(i) + '&__rnd=1554081087043'
        content = get_url(base_url, None)
        comment.write(content + b'\n')
        content = content.decode("unicode_escape")
        print(content)
    comment.close()


# if __name__ == '__main__':
#     urls = [
#         'https://test.techcomeredu.cn/TechcomerACS/loginController.do?login'
#     ]
#     ip_list = []
#     get_proxy(ip_list, 3)
#
#     for i in range(100000):
#         proxies = get_random_ip(ip_list)
#         for url in urls:
#             get_url(url, proxies)
