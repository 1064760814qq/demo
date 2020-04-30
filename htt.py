import requests
import pandas
from  bs4 import BeautifulSoup
def getHTMLtext(url):
    try:
        kv={'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers=kv)
        r.raise_for_status()
        # print(r.request.headers)
        r.encoding=r.apparent_encoding
        return r.text[1000:2000]
    except:
        return '异常'


# print(getHTMLtext('https://www.amazon.cn/dp/B00S4OK1ZS/ref=s9_acsd_hps_bw_r2_r0_1_i?pf_rd_m=A1U5RCOVU0NYF2&pf_rd_s=merchandised-search-3&pf_rd_r=4717DJ0MEH4M564PZK71&pf_rd_t=101&pf_rd_p=88665bd1-71bc-4f36-b9e1-2fd2fdd8a09f&pf_rd_i=144154071'))


def    gettext(url):
    try:
        kv={'q':'python'}
        r=requests.get(url,params=kv)
        print(r.status_code)
        print( r.request.url)
        print(len(r.text))
    except:
        print('异常')

# getzhishi('http://www.so.com/s')

def getjpg(url):
    try:
        path='D://软件/code.jpg'
        r=requests.get(url)
        print(r.status_code)
        with open(path,'wb') as f:
            f.write(r.content)
            f.close()
            print('图片保存成功')
    except:
        print('异常')

# getjpg('https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1693608873,85007695&fm=15&gp=0.jpg')

def  getip(url):
    try:
     kv={'user-agent':'Mozilla/5.0'}
     r=requests.get(url+'60.233.2.179&action=2',headers=kv)
     print(r.status_code)
     r.encoding=r.apparent_encoding
     print(r.text)
    except:
        print('异常')
# getip("https://www.ip138.com/iplookup.asp?ip=")


def  getcode(url):
    try:
        r=requests.get(url)
        # print(r.text)
        soup=BeautifulSoup(r.text,'html.parser')
        newsoup=BeautifulSoup("<b><!-- This is not a comment--></b><p>This is a commond</p>",'html.parser')
        print(newsoup.b.string)
        # tag=soup.a
        # print(soup.a.string)
        # print(tag.attrs['class'])
        # print(tag.attrs)
        # print(BeautifulSoup(r.text,'html.parser').prettify())

    except:
        print('异常')

getcode('https://www.python123.io/ws/demo.html')





