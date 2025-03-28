import os
from googleapiclient.discovery import build
import httplib2
# import requests
# from bs4 import BeautifulSoup
import yaml

"""
** 关于搜索API **
请自行创建google_config_path要求的文件google.yml，并在文件中写入以下内容：

cx: (fill in your cx id value)
api_key: (fill in your api key value)

** 关于Google联网问题 ** 
如因防火墙问题无法联网，需要配置代理。请根据需要修改proxy变量。
"""
google_config_path = '.\\credentials\\google.yml'
proxy = "http://127.0.0.1:10809"  # V2ray的默认端口，请根据需要修改

with open(google_config_path, 'r') as f:
    if proxy:
        # 设置代理
        os.environ["HTTP_PROXY"] = proxy
        os.environ["HTTPS_PROXY"] = proxy
        # 设置代理和超时时间
        http = httplib2.Http(proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP, "127.0.0.1", 10809), timeout=60)
    else:
        # 不设置代理
        http = httplib2.Http()

    # 获取google api的key和cx
    google_config = yaml.safe_load(f)
    api_key = google_config['api_key']
    cx = google_config['cx']

def google_search(query):
    """
    直接使用api搜索获得结果
    :param query: 搜索关键字
    """
    with build('customsearch', 'v1', developerKey=api_key) as service:
        print(f'=====================================================\nSearch on Google\nquery: {query}, \napi: {api_key}, \ncx: {cx}')
        res = (
            service.cse()
            .list(
                q=query,
                cx=cx
            )
            .execute(http=http)
        )
    return res.get('items', [])

# def fetch_page_content(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             paragraphs = soup.find_all('p')
#             content = ' '.join([para.get_text() for para in paragraphs])
#             return content
#         else:
#             return None
#     except Exception as e:
#         print(f'Error fetching {url}: {e}')
#         return None

# def web_search(query : str) -> str:
#     return fetch_page_content(google_search(query)[0]['link'])


if __name__ == '__main__':
    print(google_search('软件测试理论'))
    # print(fetch_page_content('Group theory'))
