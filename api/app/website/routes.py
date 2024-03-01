from flask import request
from app.website import website_bp
from app.utils.responses import response_with
from app.utils import responses as resp
from flask import Flask
import time
import requests
from bs4 import BeautifulSoup
import re
import jsonify
from urllib.parse import urljoin, urlparse
from traceback import print_exc
import json


def get_page_info(url):
    try:
        # 发送http请求获取网页内容
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string if soup.title else None
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None
        # 提取文本内容
        text_content = soup.get_text()

        # 正则表达式提取关键词
        keywords = re.findall(r'<meta\s*name=["\']keywords["\']\s*content=["\'](.*?)["\']\s*>', res.text)

        # 这里可以加入更多的信息提取逻辑
        return {
            'title': title,
            'description': description,
            'text_content': text_content,
            'keywords': keywords
        }
    except Exception as e:
        return {'error': str(e)}

def get_page_links(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        absolute_links = list(set([urljoin(url, link) for link in links]))
        new_domains = []
        for each_link in absolute_links:
            try:
                extracted_domain = each_link.split('://')[1].split('/')[0].split('?')[0]
                if extracted_domain not in new_domains and extracted_domain != url.split('://')[1].split('/')[0].split('?')[0]:
                    new_domains.append(extracted_domain)
            except IndexError as e:
                print_exc(e, f'错误URL:{url}')
                break
        # 本地数据表查询new_domains中的所有域名, 如果不在库中则入库
        
        
        print(new_domains)  # 输入的新URL包含的域名
        return absolute_links
    except Exception as e:
        print_exc(e)
        return {'error': str(e)}


@website_bp.route('/get_links/<newurl>', methods=['GET'])
def get_links_from_url(newurl):
    # print('后端函数ok')
    if ('http://' in newurl or 'https://' in newurl):
        # page_info = get_page_info(newurl)
        page_links = get_page_links(newurl)
    else:
        # page_info = get_page_info('http://' + newurl)
        page_links = get_page_links('http://' + newurl)
    print(page_links)  # list type
    # 访问每一个links,找出新的URL,并找出二级URL的所属三级URL.
    value = {'searchResults': [{'id': page_links.index(j) + 1, 'url_title': j } for j in (page_links)]}
    # print(value)
    return response_with(resp.SUCCESS_200, value=value)  # page_links