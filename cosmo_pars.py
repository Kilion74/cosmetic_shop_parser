import requests  # pip install requests
import csv
from bs4 import BeautifulSoup  # pip install bs4
import openpyxl
from openpyxl import Workbook

# pip install lxml

count = 1
while count <= 257:
    url = f'https://www.simfoniashop.ru/collection/volosy?page={count}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connactoin': 'keep-alive'}
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    category = block.find('h1', {'class': 'collection-title content-title'}).text.strip()
    print(category)
    heads = block.find_all('div', {'class': 'product_preview product_preview--collection'})
    print(len(heads))
    for i in heads:
        w = i.find_next('div', {'class': 'product_preview-preview'}).find('a', href=True)
        print('https://www.simfoniashop.ru' + w['href'])
        link = ('https://www.simfoniashop.ru' + w['href'])
        lock = requests.get(link, headers=headers).text
        base = BeautifulSoup(lock, 'lxml')
        name = base.find('h1', {'class': 'product-title content-title'}).text.strip()
        print(name)
        price = base.find('span', {'itemprop': 'price'}).text.strip()
        cena = price if price else None
        print(cena)
        articul = base.find('span', {'class': 'product-sku_field js-product-sku_field'}).text.strip()
        print(articul)
        try:
            discription = base.find('div', {'id': 'description'}).find('div',
                                                                       {'class': 'product-description editor'}).find(
                'div').text.strip()
            print(discription)
        except:
            discription = base.find('div', {'class': 'product-description editor'}).find('p').text.strip()
            print(discription)
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

        # Меняем ваш код для записи в xlsx
        storage = {
            'category': category,
            'name': name,
            'articul': articul,
            'price': cena,
            'params': '; '.join(all_param),
            'photo': pix,
            'url': link
        }

        fields = ['Category', 'Name', 'Articul', 'Price', 'Params', 'Photo', 'URL']

        # Создаём или открываем существующий файл xlsx
        file_name = f'{category}.xlsx'
        try:
            workbook = openpyxl.load_workbook(file_name)
            worksheet = workbook.active
        except FileNotFoundError:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.append(fields)  # Записываем заголовки, если файл новый

        # Записываем данные
        worksheet.append([
            storage['category'],
            storage['name'],
            storage['articul'],
            storage['price'],
            storage['params'],
            storage['photo'],
            storage['url']
        ])

        # Сохраняем изменения
        workbook.save(file_name)
    count += 1
    print(count)
