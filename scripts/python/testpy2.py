import requests
import json
import re
from bs4 import BeautifulSoup
import html2text

def save_html_to_md(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Не удалось загрузить страницу {url}.")
        return

    # Определение кодировки
    response.encoding = response.apparent_encoding

    # Парсинг HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Удаление ненужных элементов
    for img_tag in soup.find_all('img'):
        img_tag.decompose()
    for ad_tag in soup.find_all(class_='ad'):
        ad_tag.decompose()
    
    # Конвертация в Markdown
    converter = html2text.HTML2Text()
    markdown_text = converter.handle(str(soup))

    # Удаление строк до первого заголовка с #
    if '#' in markdown_text:
        markdown_text = markdown_text.split('#', 1)[1]
        markdown_text = '#' + markdown_text

    # Замена жирного текста на заголовки ##
    markdown_text = re.sub(r"\*\*(.*?)\*\*\s*", r"## \1\n", markdown_text)

    # Удаление текста в конце файла
    if "При составлении должностных" in markdown_text:
        markdown_text = markdown_text.split("При составлении должностных инструкций руководителей и специалистов ")[0]
    
    # Сохранение в файл с указанием кодировки
    with open(f"{filename}.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

# Чтение JSON-файла
with open("urls.json", "r", encoding="utf-8") as f:
    url_list = json.load(f)

# Сохранение каждой страницы из списка
for item in url_list:
    save_html_to_md(item['url'], item['name'])
