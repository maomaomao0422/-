import requests
import math
import time
import pandas as pd
import random
def get_json(url,num):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '43',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545295283,1545296925,1545297053,1545611103; _ga=GA1.2.734930496.1543924033; user_trace_token=20181204194708-5429498d-f7ba-11e8-8acb-525400f775ce; LGUID=20181204194708-54295041-f7ba-11e8-8acb-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167790b34bf1b3-0e42186f3062c08-1160684a-1327104-167790b34c00%22%2C%22%24device_id%22%3A%22167790b34bf1b3-0e42186f3062c08-1160684a-1327104-167790b34c00%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpt_baidu_pc%22%7D%7D; index_location_city=%E5%85%A8%E5%9B%BD; gate_login_token=cd486ab62ccd3c78ea862007e10f299d725d08909612c65a66a55afa5a19bb66; hasDeliver=0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; WEBTJ-ID=20181224082502-167dd99c977a-06253d977105e08-11676f4a-1327104-167dd99c97837; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1545611118; _gat=1; LGSID=20181224082502-5a768f22-0712-11e9-a64b-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu%3Ftn%3Dmonline_3_dg%26ie%3Dutf-8%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; LGRID=20181224082517-6380e3d2-0712-11e9-9a90-525400f775ce; _gid=GA1.2.1626847495.1545611103; _putrc=0B8DDDB263C033EB123F89F2B170EADC; JSESSIONID=ABAAABAAADEAAFI0BBAF11775FBA83167ABB6DE0185219E; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B70015; TG-TRACK-CODE=index_search; SEARCH_ID=555a3b6a933d42ada8fab8de9361bab5',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python%E6%88%90%E9%83%BD?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data={
        'first':'true',
        'pn':num,
        'kd':'python',
        }
    res=requests.post(url,headers=headers,data=data)
    res.raise_for_status()
    res.encoding='utf-8'
    page=res.json()
    return page

def get_page_num(count):
    res=math.ceil(count/15)
    if res>30:
        return 30
    else:
        return res

def get_page_info(jobs_list):
    page_info_list=[]
    for i in jobs_list:
        job_info=[]
        job_info.append(i['positionName'])  #职位名称
        job_info.append(i['companyFullName'])   #公司全称
        job_info.append(i['companyShortName'])  #公司简称
        job_info.append(i['companySize'])   #公司规模
        job_info.append(i['financeStage'])  #融资阶段
        job_info.append(i['district'])  #区域
        job_info.append(i['workYear'])  #工作经验
        job_info.append(i['education']) #学历要求
        job_info.append(i['salary'])    #工资
        job_info.append(i['positionAdvantage']) #职位福利
        page_info_list.append(job_info)
    return page_info_list

def main():
    url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD'
    page_1=get_json(url,1)
    total_count=page_1['content']['positionResult']['totalCount']
    num=get_page_num(total_count)
    total_info=[]
    time.sleep(random.randint(1,30))
    print('职位总数:{},页数{}'.format(total_count,num))

    for n in range(1,num+1):
        page=get_json(url,n)
        jobs_list=page['content']['positionResult']['result']
        page_info=get_page_info(jobs_list)
        total_info+=page_info
        print('已经抓取了{}页,职位总数:{}'.format(n,len(total_info)))
        time.sleep(random.randint(1,20))

    df=pd.DataFrame(data=total_info,columns=['职位名称','公司全称','公司简称','公司规模','融资阶段','区域','工作经验','学历要求','工资','职位福利'])
    df.to_csv('E:/untitled/Result.csv')

if __name__== "__main__":
    main()