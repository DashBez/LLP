import requests
from bs4 import BeautifulSoup 
from time import sleep
import re
from webapp_fashion.model import db,News


def get_html(url):
    try:
        result = requests.get(url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"})
        result.raise_for_status()
        return result.text
    except(requests.RequestException,ValueError):
        print("Сетевая ошибка")
        return False

def get_href_goods(url,name_block,key_dict,value_dict):
    html = get_html(url)
    if html:
        soup=BeautifulSoup(html,'html.parser') 
        news_list = soup(name_block, { key_dict: value_dict})
        post =[]
        for news in news_list:
            post.append(str(news)) 
        result_href = []
        for i in range(0,len(post)): 
            result_href.append({
                'href': post[i][post[i].find('href')+6:post[i].find('html')+4]
                })
        
    return result_href

def get_info_goods():
    time_to_sleep_when_captcha = 5
    Counter = 0
    Goods_info = get_href_goods("https://www.maedchenflohmarkt.de/alle-ansehen.html",'a','class','product-image orientation-portrait')
    for Goods in Goods_info:
    
        url = "https://www.maedchenflohmarkt.de"+Goods['href']
        name_block = 'div'
        key_dict = 'id'
        value_dict = 'product-detail'
        Counter = Counter +1 
        html = get_html(url)
        result_info = []
        
        if html:

            soup=BeautifulSoup(html,'html.parser')

            try:   
                part_of_Name_tmp = soup.find('div',class_='gap d-none d-sm-block').find('h1').text
                part_of_Marka_tmp = soup.find(name_block, { key_dict: value_dict}).find('div', class_='col-7 col-sm-12 d-flex align-items-stretch gap').find('a').text
                part_of_Size_tmp =  soup.find(name_block, { key_dict: value_dict}).find('p',class_= 'col-7 col-sm-12').text
                part_of_Condition_tmp = soup.find(name_block, { key_dict: value_dict}).find('div',class_='col-7 col-sm-12').find('p').text
                part_of_Description_tmp = soup.find(name_block, { key_dict: value_dict}).find("ul", {"id":"product-description"}).text
                part_of_price_tmp = soup.find(name_block, { key_dict: value_dict}).find('div',class_='d-flex flex-column align-self-center text-center product-detail__price mr-sm-3').text
                part_of_seller_tmp = soup.find(name_block, { key_dict: value_dict}).find('div',class_= 'product__seller card card-body mb-3').find('a').get('href')
                part_of_image_tmp = soup.find(name_block, { key_dict: value_dict}).find('div',class_= 'card d-none d-lg-block gap').find('img').get('src')

                result_info.append ({
                                #'url': Goods['href'],
                                'Name':part_of_Name_tmp,
                                'Marka': " ".join(part_of_Marka_tmp.split()),
                                'Size': " ".join(part_of_Size_tmp.split()),
                                'Condition': " ".join(part_of_Condition_tmp.split()),
                                'Description': str(part_of_Description_tmp),
                                'Price': " ".join(part_of_price_tmp.split()),
                                'Seller': str(part_of_seller_tmp),
                                'Image': str(part_of_image_tmp),
                                'Counter': Counter
                                #'whole part': soup.find(name_block, { key_dict: value_dict})
                
                                })
            except:
                sleep(time_to_sleep_when_captcha)
                time_to_sleep_when_captcha += 1
            for result in result_info:
                save_news(result['Name'],result['Marka'],result['Size'],result['Condition'],result['Description'],result['Price'],
                result['Seller'],result['Image'],result['Counter'])
            #return result_info
        #return False


def save_news(Name,Marka,Size,Condition,Description,Price,Seller,Image,Counter):
    news_exists = News.query.filter(News.Image == Image).count()
    #print(news_exists)
    if not news_exists:
        news_news = News(Name=Name,Marka=Marka,Size=Size,Condition=Condition,Description=Description,Price=Price,Seller=Seller,Image=Image,Counter=Counter)
        db.session.add(news_news)
        db.session.commit()

    #print(get_info_goods())
"""
if __name__ == "__main__":
    href_info = get_info_goods()

    for info in href_info:
        with open("href_info.txt",'w',encoding='utf8') as f:
            f.write(str(info))
    
"""

#print(get_info_goods())

"""

if __name__ == "__main__":    
    Goods_info = get_href_goods("https://www.maedchenflohmarkt.de/alle-ansehen.html",'a','class','product-image orientation-portrait')
    for Goods in Goods_info:
        #href_info = get_info_goods("https://www.maedchenflohmarkt.de"+Goods['href'],'div','class','product__attributes card card-body gap')
        href_info = get_info_goods("https://www.maedchenflohmarkt.de"+Goods['href'],'div','id','product-detail')
        for info in href_info:
            with open("href_info.txt",'w',encoding='utf8') as f:
                f.write(str(info))
"""
 

    

        