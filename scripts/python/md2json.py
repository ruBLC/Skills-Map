import json
import re
import os

def parse_md_to_json(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {}
    job_title_match = re.search(r'# (.+)', content)
    if job_title_match:
        result['job_title'] = job_title_match.group(1).replace('\n', ' ')

    duties_match = re.search(r'## Должностные обязанности\.\n(.+?)\n\n', content, re.S)
    if duties_match:
        result['duties'] = [duty.replace('\n', ' ') for duty in duties_match.group(1).split('. ')]

    should_know_match = re.search(r'## Должен знать:\n(.+?)\n\n', content, re.S)
    if should_know_match:
        result['should_know'] = [item.replace('\n', ' ') for item in should_know_match.group(1).split('; ')]

    qualifications_match = re.search(r'## Требования к квалификации\.\n(.+?)\n\n', content, re.S)
    if qualifications_match:
        result['qualifications'] = [item.replace('\n', ' ') for item in qualifications_match.group(1).split('; ')]

    comments_match = re.search(r'## Комментарии к должности\n(.+)', content, re.S)
    if comments_match:
        result['comments'] = comments_match.group(1).replace('\n', ' ')

    return result

def main():
    # Загрузка списка URL из JSON-файла
    with open('urls.json', 'r', encoding='utf-8') as f:
        urls_data = json.load(f)

    result = []
    for item in urls_data:
        sanitized_name = item['name'].replace(' ', '_')  # Замена пробелов на подчеркивания
        md_file_path = sanitized_name + '.md'
        if os.path.exists(md_file_path):
            parsed_data = parse_md_to_json(md_file_path)
            result.append(parsed_data)

    # Сохранение результата в JSON-файл
    with open('parsed_jobs.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
