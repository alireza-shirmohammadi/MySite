from bs4 import BeautifulSoup
import requests




page = requests.get("https://www.npr.org/sections/news/")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')



news=soup.find_all('article',attrs={"class":"item has-image has-audio"})

def Crawler():
    i = 0
    crawl = {}
    for new in news:
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
    print (crawl[2]['img'])
    print(i)
    return crawl

b=Crawler()


for i in range(len(b)):
    print(b[i]['title'])