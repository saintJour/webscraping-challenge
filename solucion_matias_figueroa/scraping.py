import requests
from bs4 import BeautifulSoup
import csv
import logging

base_url = 'http://books.toscrape.com/'
url = base_url

logging.basicConfig(level=logging.INFO)

with open('books.csv', 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = [
        'Title', 
        'Price', 
        'Stock', 
        'Category', 
        'Cover', 
        'UPC', 
        'Product Type', 
        'Price (excl. tax)', 
        'Price (incl. tax)', 
        'Tax', 
        'Availability', 
        'Number of reviews'
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    
    #iteración págs
    while(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        logging.info('Url actual: ' + url)

        #iteración libros
        for h3 in soup.find_all('h3'):
            if 'catalogue' in h3.a['href']:
                book_url = base_url + h3.a['href']
            else:
                book_url = base_url + 'catalogue/' + h3.a['href']

            book_detail = requests.get(book_url)
            book_soup = BeautifulSoup(book_detail.text, 'html.parser')

            title = book_soup.find('div', class_ = 'col-sm-6 product_main').h1.text
            price = book_soup.find('p', class_ = 'price_color').text[2:]
            stock = book_soup.find('p', class_ = 'instock availability').text[25:-17]
            category = book_soup.find('ul', class_ = 'breadcrumb').find_all('a')[2].text
            cover = base_url + book_soup.find('div', class_ = 'item active').img['src'][6:]
            upc = book_soup.find('table').find_all('td')[0].text
            product_type = book_soup.find('table').find_all('td')[1].text
            price_excl_tax = book_soup.find('table').find_all('td')[2].text[2:]
            price_incl_tax = book_soup.find('table').find_all('td')[3].text[2:]
            tax = book_soup.find('table').find_all('td')[4].text[2:]
            availability = book_soup.find('table').find_all('td')[5].text
            reviews = book_soup.find('table').find_all('td')[6].text
            
            writer.writerow({
                'Title': title, 
                'Price': price,
                'Stock': stock,
                'Category': category,
                'Cover': cover,
                'UPC': upc,
                'Product Type': product_type, 
                'Price (excl. tax)': price_excl_tax,
                'Price (incl. tax)': price_incl_tax,
                'Tax': tax, 
                'Availability': availability,
                'Number of reviews': reviews
            })

        next_li = soup.find('li', class_="next")

        if(hasattr(next_li, 'a')):
            href = next_li.a['href']
            if(href == 'catalogue/page-2.html'):
                url = base_url + href
            else:
                url = base_url + 'catalogue/' + href
        else:
            url = ''