from .models import News
from .crawler import Crawler


def News_Crawler():
    list=Crawler()
    for i in range(len(list)):
        title=list[i]['title']
        date=list[i]['date']
        short_txt=list[i]['short_txt']
        img=list[i]['img']
        if not News.objects.filter(name=title).exists():
            add=News.objects.create(name=title,short_txt=short_txt,body_txt=short_txt,date=date,picurl=img,writer='alireza')
            add.save()