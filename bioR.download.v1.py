# -*- coding: utf-8 -*-

"""
运行环境 ：Windows 系统
Python ：3.x
作者 ：魚晨光
"""
    
import requests
import re
import os
import numpy as np
import pandas as pd
import xlrd
import sys

def get_HTMLText(url):
    try:
        r=requests.get(url)
        return r.text
    except:
        return "产生异常"

def get_pks_html(urltext):

    reg = r'href="(html/.*.html)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, urltext)
    return imglist   #返回所有包的相对地址


def get_pks_addr(html_addr):

    pkn_reg=re.compile(r'html/(.*).html')
    pk_name=re.findall(pkn_reg,html_addr)[0]
    pk_text=get_HTMLText(html_addr)
    reg = r'src/contrib/([A-Za-z0-9._]*.tar.gz)'
    imgre = re.compile(reg)
    pks_gz = re.findall(imgre, pk_text)[0]
    pks_list=[pk_name, pks_gz]
    return pks_list


if __name__=="__main__":

    pks_names = []
    pks_urls = []
    lst = []
    url = "http://bioconductor.org/packages/release/bioc/"
    outdir = os.getcwd()

    text = get_HTMLText(url)
    addrs = get_pks_html(text)  #'html/a4.html'

    npaddrs = np.array(addrs)
    pknum = npaddrs.shape[0]

    #获取包的下载地址信息
    n = 1
    for j in addrs:

        pk_html=url + j
        pks_inf=get_pks_addr(pk_html)
        lst.append(pks_inf)

        pk_name = pks_inf[0]
        pk_gz = pks_inf[1]

        process = str(n) + ' / ' + str(pknum)
        print("正在获取下载地址: " + pk_name + " (" + process + ")")

        link = "http://bioconductor.org/packages/release/bioc/src/contrib/" + pk_gz
        pks_names.append(pk_name)
        pks_urls.append(link)


        np_lst = np.array(lst)
        num = np_lst.shape[0]

        """ 为测试脚本，这里只下载5个包，如果要下载所有数据，请注释掉下面两行代码： """
        if num >= 5:
            break

        n = n + 1

    pks_tab = pd.DataFrame({
        'Package': pks_names,
        'Url': pks_urls,
    })
    pks_tab.to_csv(outdir + '/' + 'biocR.urls.csv')

    sys.exit(0)