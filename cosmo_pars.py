import requests  # pip install requests
import pandas as pd  # pip install pandas
from bs4 import BeautifulSoup  # pip install bs4
import os

print(os.getcwd())
count = 1
data_list = []  # Список для хранения всех собранных данных

while count <= 257:
    url = f'https://www.simfoniashop.ru/collection/volosy?page={count}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'}
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    category = block.find('h1', {'class': 'collection-title content-title'}).text.strip()
    print(category)
    heads = block.find_all('div', {'class': 'product_preview product_preview--collection'})
    print(len(heads))

    for i in heads:
        w = i.find_next('div', {'class': 'product_preview-preview'}).find('a', href=True)
        link = 'https://www.simfoniashop.ru' + w['href']
        lock = requests.get(link, headers=headers).text
        base = BeautifulSoup(lock, 'lxml')
        name = base.find('h1', {'class': 'product-title content-title'}).text.strip()
        print(name)
        price = base.find('span', {'itemprop': 'price'}).text.strip()
        print(price)
        articul = base.find('span', {'class': 'product-sku_field js-product-sku_field'}).text.strip()
        print(articul)

        try:
            description = base.find('div', {'id': 'description'}).find('div',
                                                                       {'class': 'product-description editor'}).find(
                'div').text.strip()
            print(description)
        except:
            description = base.find('div', {'class': 'product-description editor'}).find('p').text.strip()
            print(description)

        try:
            all_param = []
            params = base.find('div', {'id': 'characteristics'}).find_all('tr')
            print(len(params))
            for param in params:
                value = ' '.join(param.text.strip().split())
                print(value)
                all_param.append(value)
        except:
            all_param = []

        pix = base.find('a', {'class': 'MagicZoom'}).find('img').get('src')
        print(pix)
        print('\n')

        # Добавляем собранные данные в список
        storage = {
            'category': category,
            'name': name,
            'articul': articul,
            'price': price,
            'params': '; '.join(all_param),
            'photo': pix
        }
        data_list.append(storage)

    count += 1
    print(count)

# Создаем DataFrame и сохраняем в Excel
df = pd.DataFrame(data_list)
df.to_excel(f'{category}.xlsx', index=False, engine='openpyxl')
print("Данные успешно сохранены в Excel!")
