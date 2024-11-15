from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import time

import random

import pandas as pd




columns = ['Başlık', 'Bağlantı', 'Makale İçeriği']
articles_data = []  


chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  

driver = webdriver.Chrome(options=chrome_options)

def scrape_page(page_num):
    try:
        url = f'https://example.com/search/{page_num}?q=choosemajor&section=articles'
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('h5', class_='card-title')

        for article in articles:
            try:
                title = article.find('a').get_text(strip=True)
                link = article.find('a', href=True)['href']
                
                print(f"Başlık: {title}")
                print(f"Bağlantı: {link}\n")
                
                content = get_article_details_selenium(link)
                
                articles_data.append([title, link, content])
            except Exception as e:
                print(f"Makale bilgisi alınırken hata oluştu: {e}")
                continue 

    except Exception as e:
        print(f"Sayfa çekilirken hata oluştu: {e}")

def get_article_details_selenium(url):
    try:
        driver.get(url)
        time.sleep(random.randint(5, 8))  

        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

       
        div_content = soup.find('div', class_='article-abstract data-section')
        
       
        if div_content:
            content = div_content.find("p")
        else:
           
            content = soup.find_all('span')
        
        if content:
            
            if isinstance(content, list):
                content_text = "".join([span.get_text(strip=True) for span in content])
            else:  
                content_text = content.get_text(strip=True)
        else:
            content_text = "Makale içeriği bulunamadı."
        
        return content_text

    except Exception as e:
        print(f"Makale içeriği çekilirken hata oluştu: {e}")
        return "Makale içeriği çekilemedi."


for page_num in range(1, 185): 
    print(f"\n=== Sayfa {page_num} ===")
    scrape_page(page_num)


df = pd.DataFrame(articles_data, columns=columns)


try:
    df.to_csv('articles2.csv', index=False, encoding='utf-8')
    print("Veriler başarıyla 'articles.csv' dosyasına kaydedildi.")
except Exception as e:
    print(f"CSV'ye kaydetme sırasında hata oluştu: {e}")


driver.quit()
