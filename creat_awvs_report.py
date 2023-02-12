#conding:utf-8
#author:胖胖小飞侠
'''
本着不重复造轮子的想法，批量扫描功能请配合其他大神的脚本使用
注意！：awvs的备注作为保存的文件名，所以在备注里最好不要出现‘/’斜杠等可能出现不标准命名规则的标点符号
此为生成漏扫报告的脚本，请确保执行该脚本之前需要保存的结果全部扫描完毕
使用前修改awvs_api
python3 creat_awvs_report.py
'''
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import time
import argparse

Awvs_url = 'https://127.0.0.1:3443' #awvs的访问url
Awvs_api = '1986123c0a5b3df4d7028d512306e936c9c72002edeef4397bc369b9c2783d807' #改为自己awvs中的api，此文件只需要改这一个就可以了
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
	'?c=800&l=100']#一般情况扫描的网站没这么多，如有需要请自行修改#每页100个，共9页，反正我想是够用的，懒人懒办法，嘻嘻嘻
def get_target_id(path):
	api_url = Awvs_url + '/api/v1/targets' + path
	r =requests.get(api_url,headers=headers,verify=False)
	data = r.json()
	target_list = data.get('targets')
	target_len = len(target_list)
	print(target_len)#每页任务数量
	for i in range(0,target_len):
		target_name = data.get('targets')[i].get('description')
		target_id = data.get('targets')[i].get('target_id')
		creat_report(target_name,target_id)
def creat_report(name,id):
	api_url = Awvs_url + '/api/v1/reports'
	data = {
		"template_id":"11111111-1111-1111-1111-111111111115",
		"source":{
			"list_type":"targets",
			"id_list":[id]
		}
	}
	data_json = json.dumps(data)
	r = requests.post(api_url,headers=headers,data=data_json,verify=False)
	print(r.json())
# get_target_id(upath[0])
def main():#生成报告但还未下载报告
	api_url = Awvs_url + '/api/v1/targets?c=100&l=100'
	r =requests.get(api_url,headers=headers,verify=False)
	data = r.json()
	all_target_num = data.get('pagination').get('count')#任务总个数
	page_num = int(all_target_num / 100)
	print('总共： ',page_num+1,'页')
	for i in range(0,page_num+1):
		print('正在爬取第',i+1,'页扫描任务')
		get_target_id(upath[i])

main()
# creat_report()
