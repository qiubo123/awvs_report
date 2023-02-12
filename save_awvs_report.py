#conding:utf-8
#author:胖胖小飞侠
'''
本着不重复造轮子的想法，批量扫描功能请配合其他大神的脚本使用
注意！：awvs的备注作为保存的文件名，所以在备注里最好不要出现‘/’斜杠等可能出现不标准命名规则的标点符号
此为报告下载脚本，请确保执行该脚本之前存在创建好的报告
试用期修改Awvs_api和文件保存路径file_save
python3 save_awvs_report.py
'''
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import time
import argparse

Awvs_url = 'https://127.0.0.1:3443' #awvs的访问url
Awvs_api = '1986123c0a5b3df4d7028d512306e936c9c72002edeef4397bc369b9c2783d807' #awvs中的api，此处需要修改
headers = {
    'X-Auth': Awvs_api,
    'Content-type': 'application/json'
}
upath = ['?l=100',
	'?c=100&l=100',
	'?c=200&l=100',
	'?c=300&l=100',
	'?c=400&l=100',
	'?c=500&l=100',
	'?c=600&l=100',
	'?c=700&l=100',
	'?c=800&l=100']
def get_down_url():#下载报告
	api_url = Awvs_url + '/api/v1/reports'
	r =requests.get(api_url,headers=headers,verify=False)
	data = r.json()
	all_target_num = data.get('pagination').get("count")
	page_num = int(all_target_num / 100)#每页100个报告，共page_num+1页
	urls = []
	for i in range(0,page_num+1):
		down_url = api_url + upath[i]
		if down_url not in urls:
			urls.append(down_url)
	print(urls)
	return urls
def down_url(down_url):
	api_url = down_url
	r =requests.get(api_url,headers=headers,verify=False)
	data = r.json().get('reports')
	report_len = len(data)
	print("当前页面共有：",report_len,"个漏洞报告需要下载")
	for i in range(0,report_len):
		f_url_path = r.json().get('reports')[i-1].get('download')[1]#0为下载html地址，1为下载PDF地址
		print(f_url_path)
		f_name = r.json().get('reports')[i-1].get('source').get('description').split(';')[1].replace('/','-')
		f_name = f_name + time.strftime('_%Y_%m_%d') + '.pdf'
		print(f_name)
		url = Awvs_url + f_url_path
		r_file = requests.get(url,headers=headers,verify=False)
		file_save = 'D:\\桌面\\py\\savepath\\'+f_name#文件目录的最后一定要有“\\”，此处需要修改
		with open(file_save,"wb") as f:
			f.write(r_file.content)
			time.sleep(1)
def main():
	for i in get_down_url():
		down_url(i)
main()