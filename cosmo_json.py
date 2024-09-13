import requests  # pip install requests
import json
from bs4 import BeautifulSoup  # pip install bs4

# pip install lxml

count = 1
my_file = []

while count <= 257:
    url = f'https://www.simfoniashop.ru/collection/volosy?page={count}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'}  # Исправлено здесь
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

        name = base.find('h1', {'class': 'product-title content-title'}).text.strip() if base.find('h1', {
            'class': 'product-title content-title'}) else 'Не указано'
        print(name)

        price = base.find('span', {'itemprop': 'price'}).text.strip() if base.find('span', {
            'itemprop': 'price'}) else 'Не указано'
        print(price)

        articul = base.find('span', {'class': 'product-sku_field js-product-sku_field'}).text.strip() if base.find(
            'span', {'class': 'product-sku_field js-product-sku_field'}) else 'Не указано'
        print(articul)

        try:
            discription = base.find('div', {'id': 'description'}).find('div',
                                                                       {'class': 'product-description editor'}).find(
                'div').text.strip()
        except:
            discription = base.find('div', {'class': 'product-description editor'}).find('p').text.strip() if base.find(
                'div', {'class': 'product-description editor'}) else 'Не указано'
        print(discription)

        all_param = []
        try:
            params = base.find('div', {'id': 'characteristics'}).find_all('tr')
            for param in params:
                value = ' '.join(param.text.strip().split())
                all_param.append(value)
        except:
            pass  # Параметры не найдены, просто пропустить
        print(len(all_param))

        pix = base.find('a', {'class': 'MagicZoom'}).find('img').get('src') if base.find('a', {
            'class': 'MagicZoom'}) else 'Не указано'
        print(pix)
        print('\n')

        my_file.append({
            'category': category,
            'name': name,
            'articul': articul,
            'price': price,
            'params': '; '.join(all_param),
            'photo': pix,
            'URL': link
        })

    # Здесь вынесено создание файла, если он отсутствует
    try:
        with open('data.json', 'r', encoding='utf-16') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Добавление новых данных к существующим
    existing_data.extend(my_file)

    with open(f'{category}.json', 'w', encoding='utf-16') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    count += 1
    print(count)
