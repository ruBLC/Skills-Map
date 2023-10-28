import requests
from bs4 import BeautifulSoup
import html2text
import chardet  # Для определения кодировки

def save_html_to_md(url):
    # Загрузка HTML-страницы
    response = requests.get(url)
    
    # Определение кодировки
    detected_encoding = chardet.detect(response.content)['encoding']
    response.encoding = detected_encoding
    
    if response.status_code != 200:
        print("Не удалось загрузить страницу.")
        return
    
    # Парсинг HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Удаление ненужных элементов, например, картинок и рекламных блоков
    for img_tag in soup.find_all('img'):
        img_tag.decompose()
    for ad_tag in soup.find_all(class_='ad'):  # предполагается, что рекламные блоки имеют класс 'ad'
        ad_tag.decompose()
    
    # Конвертация в Markdown
    converter = html2text.HTML2Text()
    markdown_text = converter.handle(str(soup))
    
    # Сохранение в файл с указанием кодировки utf-8
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)


# Пример использования
url = "http://bizlog.ru/eks/eks-5/6.htm"  # Замените на URL, который вам нужен
save_html_to_md(url)
