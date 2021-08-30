import requests
import bs4 as BeautifulSoup
import pprint
import  html5lib
import pandas as pd


def sracpeBookInfo(pageNo):  
    data = []
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    results = requests.get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    content = results.content
    soup = BeautifulSoup.BeautifulSoup(content,'html5lib')

    for book in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        name = book.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        author = book.find('a', attrs={'class':'a-size-small a-link-child'})
        rating = book.find('span', attrs={'class':'a-icon-alt'})
        price = book.find('span', attrs={'class':'p13n-sc-price'})

        refinedData = []
        if name is not None:
            refinedData.append(n[0]['alt'])
        else:
            refinedData.append("NULL")

        if author is not None:
            refinedData.append(author.text)
        else:
            refinedData.append("Unknown Author")
        if rating is not None:
            refinedData.append(rating.text)
        else:
            refinedData.append('NULL')  

        if price is not None:
            refinedData.append(price.text)
        else:
            refinedData.append('NULL')
        
        data.append(refinedData)    
    return data



if __name__ == '__main__':
    results = []
    url = "https://www.amazon.in/gp/bestsellers/books/"
    pages = 2
    for i in range(1, pages+1):
        results.append(sracpeBookInfo(i))
    flatten = lambda l: [item for sublist in l for item in sublist]
    df = pd.DataFrame(flatten(results),columns=['Book Name','Author','Rating','Price'])
    df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
    
    df = pd.read_csv("amazon_products.csv")
    print(df)