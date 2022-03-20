import requests
from bs4 import BeautifulSoup
import yarl
import os

#some global stuff
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
api_url = "https://fembed-hd.com/api/source/"
main_url = "https://fembed-hd.com/v/"
links = {}
mpv_execuatable = "mpv.exe" if os.name == "nt" else "mpv"

#functions
def get_embade_url(url):
    '''
    function to return embade url
    '''
    r=requests.get(url,headers=headers)
    src = r.content
    soup = BeautifulSoup(src,'lxml')
    
    for item in soup.find_all('a', attrs={'href':'#',"rel":"1",'data-video' : True}):
        embade_url = str(item['data-video'])
    embade_url = "https:" + embade_url
    
    return embade_url

def get_all_links(url):
    '''
    function to get all video links
    '''
    r=requests.get(url,headers=headers)
    src = r.content
    soup = BeautifulSoup(src,'lxml')
    ul_tag = soup.find('ul',attrs={'class':'list-server-items'})
    l=[item['data-video'] for item in ul_tag.find_all('li',attrs={'class':'linkserver','data-status':'1','data-video':True})]
    
    for i in l:
        u = yarl.URL(str(i))
        links[u.host] = i
        
        

    
def get_fembed_id():
    '''
    function to return fembed id
    '''
    url = links['fembed-hd.com']
    return url.split('/')[-1]
   

def generate_link(id):
    
    '''
    function to generate final streaming link
    '''
    qualities = []
    links =[]
    
    _api_url = api_url+ id
    _main_url = main_url + id
    
    r=requests.post(
        _api_url,
        headers={
            'referer': _main_url,
            'x-requested-with': 'XMLHttpRequest',
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
    )
    
    x=r.json().get('data')
    #print(x)
    for i in range(len(x)):
        qualities.append(x[i]['label'])
        links.append(x[i]['file'])
        
    print("[*]Available qualities:")
    for i in range(len(qualities)):
        print(str(i+1)+". "+qualities[i])
    
    y=int(input("[*]Enter index: "))
    l = links[y-1]
    
    #send a head request and get the real link
    r=requests.head(l,headers=headers)
    #return location header
    return r.headers['location']
    
def main():      
    link = input("[*]Enter full anime link: ")
    e_url = get_embade_url(link)
    get_all_links(e_url)
    id=get_fembed_id()
    #print(id)
    streaming_link = generate_link(id) 
    print(streaming_link)
    command = ' "'+streaming_link+'"'
    os.system(mpv_execuatable+command)
    
main()