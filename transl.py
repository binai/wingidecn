#! /etc/bin python3
# --*-- coding:utf-8 --*--

#translate WingIDE

import mstranslate,os,glob,re
import urllib.request,urllib.parse
import json,time
from http.client import *

searchname=os.path.join(os.path.dirname(__file__),'zh/*.po')
listdir=glob.glob(searchname)
clientname='Python_pi'
clientpwd='q5pwtvjZrLagc4JmMhJVdhG/1UhOylxqgNC0h2cgrmo='

# data={'key':'1125111797',
#     'keyfrom':'PythonPI',
#     'type':'data',
#     'doctype':'json',
#       'version':'1.1',
#       'q':word}
# url=r'http://fanyi.youdao.com/openapi.do?keyfrom=PythonPI&key=1125111797&type=data&doctype=json&version=1.1&q={}'

def IDtoSTR(filename):
    with open(filename,'r',encoding='utf-8') as f:
        all_content=f.readlines()
    res=all_content
    # print(all_content)
    # ts=TS(clientname,clientpwd)
    num=0
    t1=time.time()
    for k,line in enumerate(all_content):
        msgid=[]
        strbool=False
        line=line.strip()
        # print(line)
        if line.startswith('#'):
            continue
        elif line.startswith('"'):
            continue
        elif line.startswith(r'\n'):
            continue
        elif line.startswith('msgstr '):
            continue
        elif line.startswith('msgid '):
            msgid=line[6:].strip('"')
            if msgid:
                msgstr=all_content[k+1]
                msgstr=msgstr[7:].strip().strip('"')
                if not msgstr:
                    if  '%' in msgid or\
                        '_' in msgid or\
                        '#' in msgid or\
                        '-' in msgid or\
                        '[' in msgid or\
                        ']' in msgid or\
                        '<' in msgid or\
                        '>' in msgid :
                        pass
                    else:
                        strbool=True
        if strbool:
            # print(msgid)
            num+=1
            if num>900:
                t2=time.time()
                t12=t2-t2
                if t12<3600:
                    print(num,'1000次限制')
                    t_sleep=3600-t12
                    time.sleep(t_sleep)
            msgstr_ts=Yodao(msgid)
            if msgstr_ts:
                # print('{}\t=>\t{}'.format(msgid,msgstr_ts))
                msgstr_ts='msgstr "{}"\n'.format(msgstr_ts)
                if msgstr_ts.find(r'\ n')!=-1:
                    msgstr_ts=msgstr_ts.replace(r'\ n',r'\n')
                res[k+1]=msgstr_ts
    else:
        with open(filename,'w',encoding='utf-8') as f:
            f.writelines(res)

global num
num=0
def Yodao(word):

    data=[{'key':'1125111797','keyfrom':'PythonPI','type':'data',
     'doctype':'json','version':'1.1','q':word},
        {'key':'1095687459','keyfrom':'RaspberryPI','type':'data',
     'doctype':'json','version':'1.1','q':word},
        {'key':'393427090','keyfrom':'RaspberryPI1','type':'data',
     'doctype':'json','version':'1.1','q':word},
        {'key':'393427089','keyfrom':'RaspberryPI2','type':'data',
     'doctype':'json','version':'1.1','q':word}]
    url=r'http://fanyi.youdao.com/openapi.do?{}'
    html=urllib.request.urlopen(url.format(urllib.parse.urlencode(data[num%len(data)],encoding='utf-8')),timeout=30).read().decode('utf-8')
    print(html)
    res=json.loads(html)
    if res['errorCode']==0:
        if res.get('translation'):
            res=res['translation']
            return res[0]
        elif res.get('web'):
            res=[item['value'][0] for item in res['web'] if item['key'].lower()==res['query'].lower()]
            if res:
                return res[0]
    else:
        return



if __name__=="__main__":
    # test1=r'C:\ProgramFiles\Python\Wing IDE\Wing IDE 5.1.5\resources\locale\PO\zh\src_refactoring.po'
    # IDtoSTR(test1)

    #Yodao("Use Project's Home Directory")
    #"""
    #while True:
    #    for filename in listdir:
    #        IDtoSTR(filename)
    #"""
    for filename in listdir:
        #IDtoSTR(filename)
        try:
            IDtoSTR(filename)
        except BadStatusLine as e:
            print(e.line)
            time.sleep(60)
        except Exception as e:
            print('error',e)
            time.sleep(60)
        #"""
