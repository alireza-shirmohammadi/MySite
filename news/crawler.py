from bs4 import BeautifulSoup
import requests



class Crawler:

    def __init__(self,proxy=True,index=15):
        self.use_proxy = proxy
        self.index = index
        get_proxy=self.get_proxy()
        page = requests.get("https://www.npr.org/sections/news/",proxies=get_proxy)
        #print(page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.news=soup.find_all('article',attrs={"class":"item has-image"})
        print(self.news)


    def get_proxy(self):
        if self.use_proxy:
            # proxy_user = 'lwnsmdlr-{}'.format(self.index + 1)
            # proxy_address = 'http://{}:8i61xj4jgibd@p.webshare.io:80/'.format(proxy_user)
            # return {
            #   'https': proxy_address,
            #  'http': proxy_address
            # }

            proxy_user = 'lwnsmdlr-{}'.format(self.index + 1)
            proxy_address = 'http://{}:8i61xj4jgibd@p.webshare.io:80/'.format(proxy_user)
            return {
                'https': proxy_address,
                'http': proxy_address
            }
        else:
            return None
    def crawl(self):
        i = 0
        crawl = {}
        for new in self.news:
            crawl[i]={}
            #get short txt
            p=new.find('p',attrs={"class":"teaser"})
            sen = p.findNext('a').text
            counter=0
            a=""
            for word in sen.split():
                counter+=1
                if counter>4:
                    a+=" "+word
            img = new.find('img')['src']
            title=new.find('h2').text
            crawl[i]['title']=new.find('h2').text
            crawl[i]['short_txt']=a
            crawl[i]['img'] = img

            crawl[i]['date'] = new.find('time')['datetime']

            i+=1
        # print (crawl[2]['img'])
        # print(i)
        return crawl

# b=Crawler().crawl()
#
#
# for i in range(len(b)):
#     print(b[i]['title'])