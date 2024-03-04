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
from db import secondDomainScheme, thirdDomainScheme


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
    sec_oper = secondDomainScheme()
    third_oper = thirdDomainScheme()
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        res = requests.get(url, headers=headers)
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
            except Exception as e:
                print_exc()  # url.split('/')[-1]
                print(f'错误URL:{each_link}')
                break
        # 本地数据表查询new_domains中的所有域名, 如果不在库中则入库
        
        two_level_domain_nm = []
        three_level_domain_nm = []
        for _ in new_domains:  # 先判断_是几级域名再分别查询入库(只取2,3级域名) baidu.com  www.baidu.com xxx.www.baidu.com
            try:
                two_level_domain_nm.append('.'.join([_.split('.')[-2], _.split('.')[-1]]))
                three_level_domain_nm.append('.'.join([_.split('.')[-3], _.split('.')[-2], _.split('.')[-1]]))
            except Exception as e:
                print_exc()
                print(f'错误URL:{_}')
        two_level_domain_nm = list(set(two_level_domain_nm))
        three_level_domain_nm = list(set(three_level_domain_nm))
        
        for _ in two_level_domain_nm: # 写入二级域名
            if not sec_oper.query_record(second_domain=_):
                sec_oper.insert_domain(second_domain=_)
        for _ in three_level_domain_nm: # 写入三级域名
            if not third_oper.query_record(third_domain=_):
                third_oper.insert_domain(third_domain=_)
        for _ in two_level_domain_nm: # 更新当前二级域名的数量
            sec_dn_id = sec_oper.get_id_by_sec_dname(second_domain=_)
            sec_3level_num = sec_oper.query_three_level_dn_num(query_id=sec_dn_id)
            sec_oper.update_subdomain_num(second_domain=_, sub_domain_num=sec_3level_num)
        
        print(new_domains)  # 输入的新URL包含的域名
        absolute_links = [i for i in absolute_links if 'http' in i]
        return absolute_links
    except Exception as e:
        print_exc()
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